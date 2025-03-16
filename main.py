import traceback
from typing import Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai.gemini import Gemini
from db.database_manager import DatabaseManager



SERVICE_ACCOUNT_KEY_PATH = "serviceAccountKey.json"

app = FastAPI()
db_manager = DatabaseManager(SERVICE_ACCOUNT_KEY_PATH)
gemini_client = Gemini("AIzaSyCSQ72IcnYti_Jz0_q4-Yc0a0lT3y66cRA")
response =  gemini_client.generate_content("how many years do dogs live?")
print(response)

# genAI endpoints
class StartChatRequest(BaseModel):
    user_id: str #Or any user identifier.

class SendMessageRequest(BaseModel):
    session_id: str
    message: str
    
class SingleMessageRequest(BaseModel):
    message: str

@app.post("/start_chat/")
async def start_chat(request: StartChatRequest):
    """Starts a new chat session."""
    try:
        session_id = gemini_client.start_chat()
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
        response =  gemini_client.generate_content(request.message)
        return {"response": response}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/end_chat/")
async def end_chat(request: EndChatRequest):
    """Ends an existing chat session."""
    try:
        gemini_client.end_chat(request.session_id)
        return {"message": "Chat session ended successfully"}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
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

            db_manager.add_journal_entry(user_id, entry_data, date)

        return {"message": "Entries added successfully"}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/health")
async def health_check():
    """Checks if the API is running."""
    return {"status": "ok"}
