import google.generativeai as genai
from fastapi import FastAPI, HTTPException
import os
from pydantic import BaseModel
import uuid  # For generating unique session IDs

class Gemini:
    """A class to interact with the Gemini language model."""

    def __init__(self, api_key: str = None, model_name: str = 'gemini-1.5-flash'):
        """
        Initializes the Gemini class.
        """
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("API key not provided and GEMINI_API_KEY environment variable not set.")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.chat_sessions = {}  # Store chat sessions here

    def start_chat(self) -> str:
        """Starts a new chat session and returns the session ID."""
        session_id = str(uuid.uuid4())
        self.chat_sessions[session_id] = self.model.start_chat()
        return session_id

    def send_message(self, session_id: str, message: str) -> str:
        """Sends a message to an existing chat session."""
        if session_id not in self.chat_sessions:
            raise ValueError("Session not found")

        chat = self.chat_sessions[session_id]
        response = chat.send_message(message)
        return response.text
    
    def generate_content(self, message: str) -> str:
        """Generates a single response from Gemini without a chat session (async)."""
        try:
            response =  self.model.generate_content(message)
            return response.text
        except Exception as e:
            raise ValueError(f"Error generating content: {e}")

    def end_chat(self, session_id: str):
        """Ends a chat session."""
        if session_id in self.chat_sessions:
            del self.chat_sessions[session_id]
        else:
            raise ValueError("Session not found")