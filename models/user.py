from typing import List, Optional
from pydantic import BaseModel
from datetime import date

from models.journal_entry import JournalEntry
from models.user_profile import UserProfile

# Assuming you already have the JournalEntry and UserProfile models from before.
# If not, add them here.

class User(BaseModel):
    user_id: str  # Firebase Auth UID
    username: str
    firstName: str
    lastName: str
    dob: date  # Date of birth
    journalEntries: List[JournalEntry] = []  # List of journal entries
    userProfile: Optional[UserProfile] = None # Optional user profile data