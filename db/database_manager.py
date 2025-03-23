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

    def get_user_journal_entries(self, user_id: str) -> Optional[List[Dict]]:
        """Retrieves user's journal entries from Firestore and returns a list of dictionaries."""
        try:
            journal_entries_ref = self.db.collection("users").document(user_id).collection("journalEntries").stream()
            journal_entries_list = []
            for doc in journal_entries_ref:
                journal_entries_list.append(doc.to_dict())
            if journal_entries_list:
                return journal_entries_list
            else:
                return None
        except Exception as e:
            raise Exception(f"Failed to retrieve journal entries: {e}")

    def update_user_data(self, user_id: str, data: Dict):
        """Updates user data in Firestore."""
        try:
            self.db.collection("users").document(user_id).set(data)
        except Exception as e:
            raise Exception(f"Failed to update user data: {e}")

    def add_journal_entry(self, user_id: str, journal_entry: Dict):
        """Adds a single journal entry to a user's collection in Firestore."""
        try:
            user_ref = self.db.collection("users").document(user_id)
            user_ref.collection("journalEntries").document(journal_entry["date"]).set(journal_entry)
        except Exception as e:
            raise Exception(f"Failed to add journal entry: {e}")

    def get_user_persona(self, user_id: str) -> Optional[Dict]:
        """Retrieves user persona data from Firestore and returns a dictionary."""
        try:
            doc = self.db.collection("users").document(user_id).get() #assuming your user collection is called 'users'
            if doc.exists:
                data = doc.to_dict()
                if "user_persona" in data and data["user_persona"] is not None:
                    return data["user_persona"]
                else:
                    return None
            else:
                return None
        except Exception as e:
            raise Exception(f"Failed to retrieve user persona: {e}")

    def store_user_persona(self, user_persona: Dict, user_id: str):
        """Stores user persona data within the User document in Firestore."""
        try:
            user_ref = self.db.collection("users").document(user_id) #assuming your user collection is called 'users'
            user_ref.update({"user_persona": user_persona}) #store the user persona as a dictionary
        except Exception as e:
            raise Exception(f"Failed to store user persona: {e}")