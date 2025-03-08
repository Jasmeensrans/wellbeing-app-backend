from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from db.database_manager import DatabaseManager

# Replace with your service account key path
SERVICE_ACCOUNT_KEY_PATH = "serviceAccountKey.json"

app = FastAPI()
db_manager = DatabaseManager(SERVICE_ACCOUNT_KEY_PATH)

class UpdateData(BaseModel):
    user_id: str
    data: dict

@app.post("/update_user_data/")
async def update_user_data(update_data: UpdateData):
    """Updates user data in Firestore."""
    try:
        db_manager.update_user_data(update_data.user_id, update_data.data)
        return {"message": "User data updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/check_user_data/{user_id}")
async def check_user_data(user_id: str):
    """Checks the data that has been updated."""
    try:
        user_data = db_manager.get_user_data(user_id)
        if user_data:
            return user_data
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))