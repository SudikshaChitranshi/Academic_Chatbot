import json
import difflib

# Load knowledge base once at startup
with open("app/data/knowledge.json", "r") as f:
    knowledge_entries = json.load(f)

def get_knowledge_response(message: str, threshold: float = 0.6) -> str | None:
    """
    Match the user's question to known questions using fuzzy matching.
    Return the answer if similarity is above the threshold.
    """
    message = message.lower()
    best_match = None
    highest_score = 0

    for entry in knowledge_entries:
        question = entry["question"].lower()
        score = difflib.SequenceMatcher(None, message, question).ratio()
        if score > highest_score:
            highest_score = score
            best_match = entry

    if highest_score >= threshold:
        return best_match["answer"]

    return None
