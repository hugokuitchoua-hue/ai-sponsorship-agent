import os
import json
import logging
from typing import Optional, Dict
from dotenv import load_dotenv
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

def extract_best_contact(search_text: str, target_role: str) -> Optional[Dict[str, str]]:
    """
    Uses Gemini to analyze messy web search results for a SINGLE role, 
    resolve ambiguities, and return a clean JSON object.
    """
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        logger.error("GEMINI_API_KEY is missing.")
        return None

    client = genai.Client(api_key=api_key)

    system_instruction = (
        "You are an expert in B2B data extraction and OSINT. "
        "Your task is to analyze messy web search text and identify the most likely current person for a specific corporate role. "
        "If multiple people share the role, prioritize the one explicitly linked to 'France' or the highest corporate level. "
        "Return the output STRICTLY as a valid JSON object. Do not include markdown blocks like ```json."
    )

    prompt = f"""
    Target role to find: {target_role}
    
    Messy Web Data:
    ---
    {search_text}
    ---
    
    Extract the best match for the target role. 
    Format the response as a JSON object containing EXACTLY two keys: 'first_name' and 'last_name'. 
    If the person cannot be found, set the values to null.
    
    Example output format:
    {{"first_name": "Jean", "last_name": "Dupont"}}
    """

    try:
        logger.info("Gemini is extracting the exact name for the role: %s...", target_role)
        
        # Using gemini-2.0-flash (or 3.1 depending on your setup)
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite', 
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1, 
                response_mime_type="application/json", 
            )
        )
        
        extracted_data = json.loads(response.text.strip())
        return extracted_data

    except Exception as exc:
        logger.error("Failed to extract contact via AI: %s", exc)
        return None

# Local testing block
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    
    fake_tavily_output = "DECATHLON FRANCE HR Department: Mickael Cadot Human Resources Director. Jessica Dupont - Ancien Directeur."
    role = "Directeur des Ressources Humaines"
    
    result = extract_best_contact(fake_tavily_output, role)
    
    if result:
        print("\n" + "="*50)
        print("Cleaned Extracted Data (Ready for Hunter.io):")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("="*50 + "\n")