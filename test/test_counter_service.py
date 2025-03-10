import unittest
from fastapi.testclient import TestClient
import os
import sqlite3
# Enable test mode to use `metadataTest.db`
os.environ["TEST_MODE"] = "true"
from counterService.counter_service import app, get_db_connection



# Create a test client
client = TestClient(app)

class TestCalibreWeb(unittest.TestCase):
    """Unit tests for Calibre Web API"""

    def setUp(self):
        """Reset test database before each test"""
        conn = get_db_connection()
        cursor = conn.cursor()
        # Ensure the table exists before deleting rows
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                download_count INTEGER DEFAULT 0
            )
        """)
        cursor.execute("DELETE FROM books")
        cursor.execute("INSERT INTO books (id, title, download_count) VALUES (1, 'Test Book', 5)")
        cursor.execute("INSERT INTO books (id, title, download_count) VALUES (2, 'Another Book', 3)")
        conn.commit()
        conn.close()


    def print_db_state(self):
        """Helper function to print current state of database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        print("Database state:", rows)
        conn.close()

    def test_increment_download_count(self):
        #Test incrementing download count.

        response = client.post("/increment_download/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Download count incremented for book 1"})

    def test_incrementAndGet_download_count(self):
        client.post("/increment_download/1")
        response = client.get("/download_count/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("download_count"), 6)  # Should be incremented

    def test_get_download_count(self):
        """Test retrieving download count for a valid book."""
        response = client.get("/download_count/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"book_id": 1, "download_count": 5})


    def test_increment_download_count_invalid_book(self):
        """Test incrementing download count for a non-existent book."""
        response = client.post("/increment_download/999")  # Invalid book ID
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Book with ID 999 does not exist."})


    def test_get_download_count_invalid_book(self):
        """Test retrieving download count for a non-existent book."""
        response = client.get("/download_count/999")  # Invalid book ID
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Book with ID 999 does not exist."})


if __name__ == "__main__":
    unittest.main()
