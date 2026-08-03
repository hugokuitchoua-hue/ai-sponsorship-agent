import argparse
import logging
import os
from dotenv import load_dotenv

# Importation of modules for each phase of the process
from scraper import create_firecrawl_client, scrape_url
from generator import generate_sponsorship_email
from enrichment import find_company_emails
from search import find_contact_person 
from extractor import extract_best_contact 
from gmail_draft import create_gmail_draft

def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def main() -> None:
    configure_logging()
    logger = logging.getLogger(__name__)
    
    # 1. Configuration des arguments du terminal
    parser = argparse.ArgumentParser(description="AI Agent for Sponsorship Outreach & OSINT")
    parser.add_argument("company_name", help="Name of the company (e.g., 'Decathlon')")
    parser.add_argument("domain", help="Company domain for Hunter.io (e.g., 'decathlon.fr')")
    parser.add_argument("url", help="Company website URL to scrape for Firecrawl")
    parser.add_argument("--template", choices=["generic", "alumni", "rh", "rse"], default="generic", help="Email template")
    parser.add_argument("--role", default="Directeur des Ressources Humaines", help="The specific role to target")
    args = parser.parse_args()

    load_dotenv()
    
    print("\n" + "="*60)
    logger.info("STARTING AI AGENT FOR: %s", args.company_name.upper())
    print("="*60 + "\n")

    # ==========================================
    # PHASE 1 : CONTACT RESEARCH  (OSINT)
    # ==========================================
    logger.info("PHASE 1: Finding contact and email...")
    
    # A. Hunter.io -> email research
    hunter_data = find_company_emails(args.domain)
    email_pattern = hunter_data.get("pattern") if hunter_data else "{first}.{last}" 
    logger.info("Email Pattern found: %s", email_pattern)

    # B. Tavily -> web research
    raw_search_results = find_contact_person(args.company_name, args.role)
    
    constructed_email = None

    contact_full_name = None
    
    if raw_search_results:
        # C. Gemini -> cleanning and extracting the best contact
        person = extract_best_contact(raw_search_results, args.role)
        
        print("\nCONTACT IDENTIFIED:")
        if person and person.get("first_name") and person.get("last_name"):
            # Capitalization and formatting
            first = person["first_name"].lower()
            last = person["last_name"].lower()
            contact_full_name = f"{first.capitalize()} {last.capitalize()}"
            # Construction of the email based on the pattern
            local_part = email_pattern.replace("{first}", first).replace("{last}", last)
            
            # If the local part doesn't contain an '@', we append the domain to form a complete email address
            if "@" not in local_part:
                constructed_email = f"{local_part}@{args.domain}"
            else:
                constructed_email = local_part
            print(f"- {args.role} : {first.capitalize()} {last.capitalize()} -> {constructed_email}")
        else:
            print(f"- {args.role} : No confident match found.")
    else:
        logger.warning("No search results found to extract contact.")
    print("\n")

    # ==========================================
    # PHASE 2 : SCRAPING & REDACTION (IA)
    # ==========================================
    logger.info("PHASE 2: Scraping website and generating email...")
    
    firecrawl_key = os.getenv("FIRECRAWL_API_KEY")
    if not firecrawl_key:
        logger.error("FIRECRAWL_API_KEY is missing.")
        return
        
    client = create_firecrawl_client(firecrawl_key)
    
    document_data = scrape_url(client, args.url, formats=["markdown"])
    markdown_content = document_data.get("markdown", "")

    if not markdown_content:
        logger.error("No markdown content found to generate email.")
        return

    # PHASE 3 : EMAIL GENERATION
    email_draft = generate_sponsorship_email(args.company_name, markdown_content, args.template, contact_full_name)

    if email_draft:
        print("\n" + "=" * 60)
        print("FINAL EMAIL DRAFT:")
        print("=" * 60)
        print(email_draft)
        if constructed_email:
            print(f"\n To send : {constructed_email}")
        print("=" * 60 + "\n")
        
        # save the draft to Gmail if we have a constructed email
        safe_name = args.company_name.replace(" ", "_").lower()
        if email_draft:
            print("\n" + "=" * 60)
            print("FINAL EMAIL DRAFT:")
            print("=" * 60)
            print(email_draft)
        if constructed_email:
            print(f"\n To send : {constructed_email}")
        print("=" * 60 + "\n")
        
        # Save the draft to Gmail if we have a constructed email
        if constructed_email:
            # Extract the subject line from the email draft if it exists, otherwise use a default subject
            subject = "Partenariat Cartel des Mines 2027"
            first_line = email_draft.split('\n')[0]
            if "Objet" in first_line:
                subject = first_line.replace("Objet :", "").replace("Objet:", "").strip()
                # Remove the subject line from the email body to avoid duplication
                email_body = "\n".join(email_draft.split('\n')[1:]).strip()
            else:
                email_body = email_draft
            
            create_gmail_draft(to_email=constructed_email, subject=subject, message_body=email_body)
        else:
            logger.warning(" No constructed email available. Skipping Gmail draft creation.")

if __name__ == "__main__":
    main()