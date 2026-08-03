import os
import logging
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def find_company_emails(domain: str) -> Optional[Dict[str, Any]]:
    """
    Uses Hunter.io Domain Search API to find the email pattern 
    and public emails associated with a given company domain.
    """
    load_dotenv()
    api_key = os.getenv("HUNTER_API_KEY")

    if not api_key:
        logger.error("HUNTER_API_KEY is missing from the .env file.")
        return None

    # Hunter.io Domain Search API Endpoint
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}"

    try:
        logger.info("Searching for email contacts at %s...", domain)
        response = requests.get(url)
        response.raise_for_status() # Raises an error for bad HTTP status codes
        
        data = response.json()

        if "data" in data:
            pattern = data["data"].get("pattern", "No exact pattern found")
            emails = data["data"].get("emails", [])

            result = {
                "domain": domain,
                "pattern": pattern,
                "contacts": []
            }

            # Extract the top 5 most relevant contacts to save tokens later
            for email_data in emails[:5]: 
                result["contacts"].append({
                    "email": email_data.get("value"),
                    "first_name": email_data.get("first_name"),
                    "last_name": email_data.get("last_name"),
                    "position": email_data.get("position"),
                    "department": email_data.get("department")
                })
            return result
            
        return None

    except requests.exceptions.RequestException as exc:
        logger.error("Hunter.io API request failed: %s", exc)
        return None

# Local execution block for testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    
    # Test with a known domain
    test_domain = "decathlon.fr"
    contacts = find_company_emails(test_domain)
    
    if contacts:
        print("\n" + "="*50)
        print(f"Domain: {contacts['domain']}")
        print(f"Email Pattern: {contacts['pattern']}")
        print("\nTop Contacts Found:")
        for c in contacts['contacts']:
            dept = c['department'] if c['department'] else "Unknown Dept"
            print(f"- {c['first_name']} {c['last_name']} ({dept}) | Role: {c['position']} | {c['email']}")
        print("="*50 + "\n")