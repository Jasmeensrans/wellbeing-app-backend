
import json
from typing import Dict, List
from models.user_profile import UserPersona


def map_dict_to_string(data: dict, indent: int = 0) -> str:
    """
    Maps a dictionary to a string representation, handling nested dictionaries.

    Args:
        data: The dictionary to map.
        indent: The current indentation level.

    Returns:
        A string representation of the dictionary.
    """
    result = ""
    indent_str = "  " * indent  # 2 spaces per indent level

    for key, value in data.items():
        if isinstance(value, dict):
            result += f"{indent_str}{key}:\n{map_dict_to_string(value, indent + 1)}"
        else:
            result += f"{indent_str}{key}: {value}\n"
    return result

def get_initial_chat_prompt(user_profile: Dict, journal_entries: List[Dict]) -> str:
    """
    Generates the initial chat prompt for a therapy session, incorporating user profile and journal entries.

    Args:
        user_profile: The user's profile data.
        journal_entries: A list of the user's journal entries.

    Returns:
        The initial chat prompt as a string.
    """
    journal_entries_str = ''
    if journal_entries:
        for entry in journal_entries:
            
            journal_entries_str += map_dict_to_string(entry)
    persona_data_str = map_dict_to_string(user_profile) if user_profile else ""
    prompt = f"""
    You are a compassionate and supportive virtual well-being coach. Your primary role is to provide a safe and empathetic space for users to explore their feelings, thoughts, and experiences related to their mental and emotional well-being.

    Your goal is to actively listen, ask clarifying questions, and offer gentle guidance, drawing from established therapeutic principles such as Cognitive Behavioral Therapy (CBT) and mindfulness.

    **User's Journal Entries:**

    {journal_entries_str}

    **User's Persona Data:**

    {persona_data_str}

    **Important Guidelines:**

    * **Empathy and Validation:** Always acknowledge and validate the user's feelings. Use phrases like, "I understand," "That sounds difficult," or "It's okay to feel that way."
    * **Active Listening:** Pay close attention to the user's words and tone. Reflect back what you hear to ensure understanding.
    * **Clarifying Questions:** Ask open-ended questions to encourage the user to elaborate on their thoughts and feelings.
    * **Non-Judgmental Approach:** Avoid making judgments or offering unsolicited advice.
    * **Focus on Coping Mechanisms:** Help users identify and develop healthy coping mechanisms for managing stress, anxiety, and other challenges.
    * **Do NOT Provide Medical Diagnoses or Prescribe Medication:** You are not a medical professional. If a user expresses concerns about their physical or mental health, advise them to seek professional help from a qualified healthcare provider.
    * **Safety First:** If a user expresses thoughts of self-harm or harm to others, immediately advise them to contact a crisis hotline or emergency services.
    * **Confidentiality:** Assure the user that their conversations are confidential and secure.
    * **Contextual Awareness:** Use the provided context from the user's journal entries and persona data to tailor your responses.
    * **Respect User Autonomy:** Encourage users to make their own choices and decisions.
    * **Positive Reinforcement:** Offer positive reinforcement and encouragement for the user's efforts to improve their well-being.
    * **Therapeutic Focus:** Your responses should be strictly limited to topics related to mental and emotional well-being, stress management, coping mechanisms, and related therapeutic techniques. **Do not provide advice, solutions, or specific information related to the user's external activities, including but not limited to, professional work, sports, finances, or any other domain outside of mental health.** If the user discusses external issues, focus solely on the emotional impact and stress they experience, rather than offering specific solutions or information related to those external domains.

    **Starting the Session:**

    "Welcome to your therapy session. Based on your journal entries and persona data, I understand [mention a relevant observation or summary, for example, based on recent mood fluctuations]. I'm here to listen and support you. How are you feeling today? Is there anything specific you'd like to talk about?"
    """
    return prompt

def get_closing_chat_prompt(user_profile: Dict) -> str:
    """
    Generates the closing chat prompt for a therapy session, incorporating user profile and chat log.

    Args:
        user_profile: The user's profile data.
        chat_log: The chat log of the session.

    Returns:
        The closing chat prompt as a string.
    """
    user_profile_json = 'empty user profile'
    if user_profile:
        user_profile_json = map_dict_to_string(user_profile)

    prompt = f"""
    You are an AI assistant tasked with summarizing a therapy session and updating a user's profile based on the conversation. The session has concluded. Please analyze the following conversation and update the user's profile according to the provided schema.

    **User Profile Schema:**

    ```json
    {user_profile_json}
    Instructions:

    Analyze the Conversation: Carefully review the entire conversation, paying attention to the user's statements, emotions, and behaviors.
    Update the User Profile: Populate the JSON structure with the information extracted from the conversation.
    userId: Retain the user's ID.
    presentingSymptoms: List any symptoms the user mentioned.
    observedPatterns: Identify recurring patterns in the user's thoughts, feelings, or behaviors.
    observedMood: Summarize the user's overall mood trend and any recent fluctuations.
    observedBehavior: Note any observed avoidance behaviors or issues with concentration.
    currentGoals: List the user's current goals and their progress.
    keyThemes: Identify the main themes discussed during the session.
    significantEvents: List any significant events mentioned by the user.
    suggestedAssignments: List any assignments suggested during the session and whether they were completed (if applicable).
    chatLog: Copy the chat log into the structure.
    JSON Output: Ensure the output is a valid JSON object that can be parsed by a Python application.
    Conciseness: Be concise and accurate in your summaries.
    Accuracy: do not add any information that was not said in the chat log.
    Output:

    [Generate the JSON output here.]
    """
    
    return prompt
    
def get_correlation_prompt_cot(articles: List[Dict]) -> str:
    """
    Generates a prompt to find correlations from a list of articles, using chain-of-thought prompting
    Args:
        articles: A list of dictionaries, where each dictionary represents an article.

    Returns:
        A string representing the correlation prompt.
    """

    # Load example entries from COT_exaple_entries.json
    try:
        with open("COT_exaple_entries.json", "r") as f:
            example_entries = json.load(f)
    except FileNotFoundError:
        example_entries = [{"Sleep Duration": "8 hours", "Exercise": "Intense, 2 hours", "Sleep Quality": "Good"},
                           {"Sleep Duration": "5 hours", "Caffeine": "120mg", "Sleep Quality": "Poor"},
                           {"Sleep Duration": "8 hours", "Exercise": "Intense, 2 hours", "Mood": "Positive"}]

    example_entries_str = "\n".join([str(entry) for entry in example_entries])

    articles_str = "\n".join([str(article) for article in articles])

    prompt = f"""
    Q. What correlations do you notice from the following journal entries {example_entries_str}
    Explanation:
    Sleep duration and quality was better with intense and long exercise. Sleep duration and quality was poor with high consumption of caffine (120mg). Mood was more positive with good sleep and intensive exervcise
    Answer: Better sleep has been correlated with exercise. High consumption of caffiene has been correlated with poor sleep. Positive mood has been correlated with good sleep and exercise
    Q. What correlations do you notice in the following articles {articles_str}. Make sure your answer is around 300 characters
    Answer:
    """
    return prompt