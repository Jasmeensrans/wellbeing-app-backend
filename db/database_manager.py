import firebase_admin
from firebase_admin import credentials, firestore
from typing import Dict, List, Optional
from pydantic import BaseModel

class DatabaseManager:
    """Handles Firebase Firestore database operations."""

    def __init__(self, service_account_key_path: str):
        """Initializes the DatabaseManager."""
        try:
            cred = credentials.Certificate(service_account_key_path)
            firebase_admin.initialize_app(cred)
            self.db = firestore.client()

        except Exception as e:
            raise Exception(f"Database initialization failed: {e}")

    def get_user_data(self, user_id: str) -> Optional[Dict]:
        """Retrieves user data from Firestore."""
        try:
            doc = self.db.collection("users").document(user_id).get()
            if doc.exists:
                return doc.to_dict()
            else:
                return None
        except Exception as e:
            raise Exception(f"Failed to retrieve user data: {e}")

    def get_user_journal_entries(self, user_id: str) -> List[Dict]:
        """Retrieves user's journal entries from Firestore."""
        try:
            journal_entries_ref = self.db.collection("users").document(user_id).collection("journalEntries").stream()
            journal_entries = [doc.to_dict() for doc in journal_entries_ref]
            return journal_entries
        except Exception as e:
            raise Exception(f"Failed to retrieve journal entries: {e}")

    def update_user_data(self, user_id: str, data: Dict):
        """Updates user data in Firestore."""
        try:
            self.db.collection("users").document(user_id).set(data)
        except Exception as e:
            raise Exception(f"Failed to update user data: {e}")