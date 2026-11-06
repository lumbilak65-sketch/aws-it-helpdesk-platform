import tempfile
import unittest
from pathlib import Path

import local_app


class LocalHelpDeskTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        local_app.app.config.update(
            TESTING=True,
            DATABASE=str(Path(self.temp_dir.name) / "test.sqlite3"),
        )
        local_app.init_db()
        self.client = local_app.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_dashboard_shows_seed_ticket(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"VPN connection issue", response.data)

    def test_create_ticket_and_open_details(self):
        response = self.client.post(
            "/",
            data={
                "title": "Printer not working",
                "description": "The printer is offline.",
                "requester": "person@example.com",
                "priority": "Medium",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Printer not working", response.data)

    def test_ticket_status_can_be_updated(self):
        response = self.client.post("/tickets/1", data={"status": "In Progress"})
        self.assertEqual(response.status_code, 302)
        detail = self.client.get("/tickets/1")
        self.assertIn(b"In Progress", detail.data)

    def test_unknown_ticket_returns_not_found(self):
        response = self.client.get("/tickets/999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()

