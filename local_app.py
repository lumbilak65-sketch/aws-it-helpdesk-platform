"""Local, AWS-free demo for the AWS IT Help Desk Platform portfolio project."""

from datetime import datetime, timezone
from contextlib import contextmanager
import os
from pathlib import Path
import sqlite3

from flask import Flask, abort, flash, redirect, render_template, request, url_for


app = Flask(__name__)
app.config["SECRET_KEY"] = "local-demo-only-change-before-deployment"
app.config["DATABASE"] = os.environ.get(
    "HELPDESK_DATABASE", str(Path(__file__).parent / "instance" / "helpdesk.sqlite3")
)

PRIORITIES = {"Low", "Medium", "High", "Critical"}
STATUSES = {"Open", "In Progress", "Resolved"}


def connect_db():
    database = app.config["DATABASE"]
    Path(database).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row
    return connection


@contextmanager
def database():
    connection = connect_db()
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def init_db():
    with database() as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                priority TEXT NOT NULL,
                requester TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Open',
                created_at TEXT NOT NULL
            )"""
        )
        count = connection.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
        if count == 0:
            connection.execute(
                """INSERT INTO tickets
                (title, description, priority, requester, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    "VPN connection issue",
                    "A staff member cannot connect to the company VPN. Check account status and network access.",
                    "High",
                    "alex@example.com",
                    "Open",
                    datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
                ),
            )


@app.route("/", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        requester = request.form.get("requester", "").strip()
        priority = request.form.get("priority", "Medium")
        if not title or not description or not requester:
            flash("Please fill in the title, description, and requester.", "error")
        elif priority not in PRIORITIES:
            flash("Choose one of the listed priority levels.", "error")
        else:
            with database() as connection:
                connection.execute(
                    """INSERT INTO tickets
                    (title, description, priority, requester, status, created_at)
                    VALUES (?, ?, ?, ?, 'Open', ?)""",
                    (
                        title,
                        description,
                        priority,
                        requester,
                        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
                    ),
                )
            flash("Ticket created successfully.", "success")
            return redirect(url_for("dashboard"))

    with database() as connection:
        tickets = connection.execute(
            "SELECT * FROM tickets ORDER BY id DESC"
        ).fetchall()
    stats = {
        "total": len(tickets),
        "open": sum(ticket["status"] == "Open" for ticket in tickets),
        "progress": sum(ticket["status"] == "In Progress" for ticket in tickets),
        "resolved": sum(ticket["status"] == "Resolved" for ticket in tickets),
    }
    return render_template("local_dashboard.html", tickets=tickets, stats=stats)


@app.route("/tickets/<int:ticket_id>", methods=["GET", "POST"])
def ticket_detail(ticket_id):
    if request.method == "POST":
        status = request.form.get("status", "")
        if status not in STATUSES:
            abort(400)
        with database() as connection:
            cursor = connection.execute(
                "UPDATE tickets SET status = ? WHERE id = ?", (status, ticket_id)
            )
            if cursor.rowcount == 0:
                abort(404)
        flash("Ticket status updated.", "success")
        return redirect(url_for("ticket_detail", ticket_id=ticket_id))

    with database() as connection:
        ticket = connection.execute(
            "SELECT * FROM tickets WHERE id = ?", (ticket_id,)
        ).fetchone()
    if ticket is None:
        abort(404)
    return render_template("local_ticket.html", ticket=ticket, statuses=sorted(STATUSES))


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5001, debug=False)

