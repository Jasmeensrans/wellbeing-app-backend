import json
import traceback
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai.gemini import Gemini
from ai.prompt import get_correlation_prompt_cot, get_initial_chat_prompt
from db.database_manager import DatabaseManager
from utils.entry_utils import get_entries_by_date_range

SERVICE_ACCOUNT_KEY_PATH = "serviceAccountKey.json"

app = FastAPI()
db_manager = DatabaseManager(SERVICE_ACCOUNT_KEY_PATH)
gemini_client = Gemini("AIzaSyCSQ72IcnYti_Jz0_q4-Yc0a0lT3y66cRA")

# genAI endpoints
class StartChatRequest(BaseModel):
    user_id: str  # Or any user identifier.

class EndChatRequest(BaseModel):
    user_id: str  # Or any user identifier.
    session_id: str

class SendMessageRequest(BaseModel):
    session_id: str
    message: str

class SingleMessageRequest(BaseModel):
    message: str

class CorrelationRequest(BaseModel):
    user_id: str
    start_date: str
    end_date: str


# Chat endpoints
@app.post("/start_chat/")
async def start_chat(request: StartChatRequest):
    """Starts a new chat session."""
    try:
        session_id = gemini_client.start_chat()
        # get the users journal entries using the user_id
        journal_entries = db_manager.get_user_journal_entries(request.user_id)
        # get user persona
        user_persona = db_manager.get_user_persona(request.user_id)

        # prompt chat with the journal entries to set context
        prefix_prompt = get_initial_chat_prompt(user_persona, journal_entries)
        gemini_client.send_message(session_id, prefix_prompt)
        return {"session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send_message/")
async def send_message(request: SendMessageRequest):
    """Sends a message to an existing chat session."""
    try:
        response = gemini_client.send_message(request.session_id, request.message)
        return {"response": response}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get_single_response/")
async def get_single_response(request: SingleMessageRequest):
    """Sends a message to an existing chat session."""
    try:
        response = gemini_client.generate_content(request.message)
        return {"response": response}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/end_chat/")
async def end_chat(request: EndChatRequest):
    """Ends an existing chat session."""
    try:
        # send the closing prompt to gemini and update the user personal in firebase
        # TODO: fix this later
        # current_user_persona = db_manager.get_user_persona(request.user_id)
        # closing_prompt = getClosingChatPrompt(current_user_persona)
        # new_persona_json = gemini_client.send_message(request.session_id, closing_prompt)
        # data = json.loads(new_persona_json) # this fails!!
        # db_manager.store_user_persona(data["userProfile"], request.user_id)
        gemini_client.end_chat(request.session_id)
        return {"message": "Chat session ended successfully"}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Correlation/Insights endpoints
@app.post("/get_correlations/")
async def get_correlations(request: CorrelationRequest):
    try:
        # Fetch journal entries within the specified date range for the user
        entries = db_manager.get_user_journal_entries(request.user_id)

        #Filter the journal entries by date range, using the helper function.
        filtered_entries = get_entries_by_date_range(entries, request.start_date, request.end_date)
        print(filtered_entries)
        # Create prompt
        prompt = get_correlation_prompt_cot(filtered_entries)

        # Fetch response
        response = gemini_client.generate_content(prompt)
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# function to add mock data to firebase
# add a user
class UserData(BaseModel):
    user_id: str
    user_data: Dict

@app.post("/add_user/")
async def add_user(user_data: UserData):
    """Adds a user to Firestore."""
    try:
        db_manager.add_user(user_data.user_id, user_data.user_data)
        return {"message": "User added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# add list of entries for a given user
@app.post("/add_entries/")
async def add_entries(data: Dict):
    """Adds a list of entries to a user's collection in Firestore."""
    try:
        user_id = data.get("user_id")
        entries = data.get("journal_entries")

        if not user_id or not entries or not isinstance(entries, list):
            raise HTTPException(status_code=400, detail="Invalid request format")

        for entry in entries:
            date = entry.get("date")
            entry_data = entry

            if not date or not isinstance(entry_data, dict):
                raise HTTPException(status_code=400, detail="Invalid entry format")

            db_manager.add_journal_entry(user_id, entry_data)

        return {"message": "Entries added successfully"}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Checks if the API is running."""
    return {"status": "ok"}