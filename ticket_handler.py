import json
import os
import uuid
from datetime import datetime, timezone

import boto3

TABLE_NAME = os.environ.get("TABLE_NAME", "ITHelpDeskTickets")
table = boto3.resource("dynamodb").Table(TABLE_NAME)

def response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }

def lambda_handler(event, context):
    method = event.get("httpMethod", "POST")
    if method == "POST":
        body = json.loads(event.get("body") or "{}")
        if not body.get("title") or not body.get("description"):
            return response(400, {"error": "title and description are required"})

        ticket_id = str(uuid.uuid4())
        item = {
            "TicketId": ticket_id,
            "Title": body["title"],
            "Description": body["description"],
            "Priority": body.get("priority", "Medium"),
            "Requester": body.get("requester", "unknown"),
            "Status": "Open",
            "CreatedAt": datetime.now(timezone.utc).isoformat(),
        }
        table.put_item(Item=item)
        return response(201, item)

    if method == "GET":
        ticket_id = (event.get("pathParameters") or {}).get("ticketId")
        if not ticket_id:
            return response(400, {"error": "ticketId is required"})
        result = table.get_item(Key={"TicketId": ticket_id})
        item = result.get("Item")
        return response(200 if item else 404, item or {"error": "ticket not found"})

    return response(405, {"error": "method not allowed"})
