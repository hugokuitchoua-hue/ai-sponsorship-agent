import os
import logging
import re
from typing import Optional
from dotenv import load_dotenv
from tavily import TavilyClient

logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """
    Cleans the raw text to save LLM tokens by removing 
    excessive whitespace, newlines, and social media artifacts.
    """
    if not text:
        return ""
    # Remove multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    # Remove common useless artifacts from LinkedIn scraping
    text = re.sub(r'\[Likes:.*?\]|profile photo|N/A|gmail\.com', '', text, flags=re.IGNORECASE)
    return text.strip()

def find_contact_person(company_name: str, target_role: str) -> Optional[str]:
    """
    Uses Tavily Search API to find the specific contact person.
    Utilizes 'include_answer' to drastically reduce LLM token consumption.
    """
    load_dotenv()
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        logger.error("TAVILY_API_KEY is missing from the .env file.")
        return None

    try:
        client = TavilyClient(api_key=api_key)
        
        # A more conversational query often works better for the answer generation
        query = f"Who is the {target_role} at {company_name} in France? LinkedIn"
        logger.info("Searching the web for: '%s'...", query)
        
        # Call Tavily API with include_answer=True (The Magic Bullet)
        response = client.search(
            query=query,
            search_depth="basic",
            include_answer=True, # Tavily will synthesize a short answer!
            max_results=3 # We don't need more than 3 for a specific role
        )
        
        # 1. Prioritize the short, synthesized answer
        synthesized_answer = response.get("answer")
        if synthesized_answer:
            logger.info("Tavily synthesized a clean answer.")
            return clean_text(synthesized_answer)
            
        # 2. Fallback: Aggregate and clean the snippets if no direct answer
        logger.warning("No synthesized answer, falling back to snippets.")
        results_text = ""
        for result in response.get("results", []):
            results_text += f"- {result.get('content')}\n"
            
        cleaned_text = clean_text(results_text)
        
        if cleaned_text:
            # Hard limit to 1000 characters to protect Gemini token limits
            return cleaned_text[:1000] 
        else:
            return None

    except Exception as exc:
        logger.error("Tavily API request failed: %s", exc)
        return None

# Local testing block
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    
    test_company = "Decathlon"
    test_role = "Directeur des Ressources Humaines"
    
    search_data = find_contact_person(test_company, test_role)
    
    if search_data:
        print("\n" + "="*60)
        print(f"Company: {test_company}")
        print(f"Target Role: {test_role}")
        print("\nWeb Search Results (Cleaned):\n")
        print(search_data)
        print("\n" + "="*60)
