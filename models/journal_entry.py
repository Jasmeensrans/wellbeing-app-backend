from typing import List, Optional
from pydantic import BaseModel, Field

class Sleep(BaseModel):
    hours: float
    quality: str
    awakenings: int

class Diet(BaseModel):
    generalDiet: str
    sugarConsumption: str
    caffeineIntake: str
    alcoholConsumption: str
    waterIntake: str

class Exercise(BaseModel):
    duration: int
    type: str
    intensity: str

class Mood(BaseModel):
    overall: int
    specificMood: List[str]
    stressLevel: int

class MenstrualCycle(BaseModel):
    phase: str
    symptoms: List[str]

class JournalEntry(BaseModel):
    date: str
    sleep: Sleep
    diet: Diet
    exercise: Exercise
    mood: Mood
    menstrualCycle: MenstrualCycle
    creativeTime: int
    socialInteractions: int
    screenTime: int
    dailySpending: int
    feelingAboutFinances: str
    timeOutside: int
    dailyGratitude: List[str]
    dailyJournal: str

class JournalEntries(BaseModel):
    journalEntries: List[JournalEntry]