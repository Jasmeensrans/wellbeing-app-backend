from typing import List, Optional
from pydantic import BaseModel, Field

class Goal(BaseModel):
    goal: str
    progress: str

class SignificantEvent(BaseModel):
    event: str
    date: str

class SuggestedAssignment(BaseModel):
    assignment: str
    completed: bool

class SelfAssessmentResult(BaseModel):
    scale: str
    score: int
    date: str

class ChatLogEntry(BaseModel):
    timestamp: str
    userMessage: str
    aiMessage: str

class ObservedMood(BaseModel):
    overallTrend: str
    recentFluctuations: str

class ObservedBehavior(BaseModel):
    avoidance: str
    concentration: str

class UserProfile(BaseModel):
    userId: str
    presentingSymptoms: List[str]
    observedPatterns: List[str]
    observedMood: ObservedMood
    observedBehavior: ObservedBehavior
    currentGoals: List[Goal]
    keyThemes: List[str]
    significantEvents: List[SignificantEvent]
    suggestedAssignments: List[SuggestedAssignment]
    selfAssessmentResults: List[SelfAssessmentResult]
    chatLog: List[ChatLogEntry]

class UserProfileData(BaseModel):
    userProfile: UserProfile
    