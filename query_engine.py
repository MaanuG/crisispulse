from typing import List
import spacy

# =========================================================
# LOAD SPACY MODEL
# =========================================================

# Install:
# pip install spacy
# python -m spacy download en_core_web_sm

nlp = spacy.load("en_core_web_sm")


# =========================================================
# CRISIS TYPES
# =========================================================

CRISIS_TYPES = {

    # Natural disasters
    "earthquake",
    "wildfire",
    "fire",
    "flood",
    "flooding",
    "hurricane",
    "tornado",
    "tsunami",
    "landslide",
    "cyclone",
    "typhoon",
    "storm",
    "blizzard",
    "avalanche",
    "drought",
    "heatwave",
    "volcano",
    "eruption",

    # Humanitarian crises
    "famine",
    "hunger",
    "starvation",
    "refugees",
    "displacement",
    "evacuation",
    "homelessness",
    "poverty",
    "shortage",

    # Conflict / violence
    "shooting",
    "attack",
    "bombing",
    "explosion",
    "terrorism",
    "terrorist",
    "war",
    "conflict",
    "invasion",
    "airstrike",
    "riot",
    "violence",
    "hostage",
    "kidnapping",

    # Infrastructure / outages
    "blackout",
    "outage",
    "power outage",
    "internet outage",
    "water outage",
    "grid failure",
    "cyberattack",
    "hack",
    "data breach",

    # Public health
    "pandemic",
    "epidemic",
    "outbreak",
    "virus",
    "disease",
    "cholera",
    "covid",
    "flu",

    # Economic / supply chain
    "inflation",
    "recession",
    "collapse",
    "strike",
    "shortages",
    "layoffs",

    # Environmental
    "pollution",
    "contamination",
    "oil spill",
    "radiation",
    "toxic leak",

    # Transportation / industrial
    "plane crash",
    "train derailment",
    "shipwreck",
    "factory explosion",
    "chemical spill"
}


# =========================================================
# EXTRACT CLEAN EVENT QUERY
# =========================================================

def extract_event_query(claim: str) -> str:

    doc = nlp(claim)

    disaster = None
    important_words = []

    # -----------------------------------------
    # Find crisis keyword
    # -----------------------------------------

    for token in doc:

        word = token.text.lower()

        if word in CRISIS_TYPES:
            disaster = token.text

    # -----------------------------------------
    # Keep:
    # - Proper nouns
    # - Crisis keywords
    # -----------------------------------------

    for token in doc:

        if (
            token.pos_ == "PROPN"
            or token.text.lower() in CRISIS_TYPES
        ):

            clean = token.text.strip()

            if clean not in important_words:
                important_words.append(clean)

    # Ensure disaster word included
    if disaster and disaster not in important_words:
        important_words.append(disaster)

    query = " ".join(important_words)

    return query if query else claim


# =========================================================
# GENERATE SEARCH QUERIES
# =========================================================

def generate_search_queries(user_input: str) -> List[str]:
    """
    Converts natural-language claims into optimized
    Reddit/news search queries.

    Example:
    "The Philippines Mindanao earthquake is causing massive casualties"

    ->
    ["Philippines Mindanao earthquake"]
    """

    optimized_query = extract_event_query(user_input)
    return [optimized_query]

