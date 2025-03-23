from typing import List
from pydantic import BaseModel

class Goal(BaseModel):
    goal: str
    progress: str


class SuggestedAssignment(BaseModel):
    assignment: str
    completed: bool


class ObservedMood(BaseModel):
    overallTrend: str
    recentFluctuations: str

class ObservedBehavior(BaseModel):
    avoidance: str
    concentration: str

class UserPersona(BaseModel):
    userId: str
    presentingSymptoms: List[str]
    observedPatterns: List[str]
    observedMood: ObservedMood
    observedBehavior: ObservedBehavior
    currentGoals: List[Goal]
    keyThemes: List[str]
    significantEvents: List[str]
    suggestedAssignments: List[SuggestedAssignment]

class UserPersonaData(BaseModel):
    userProfile: UserPersona
    