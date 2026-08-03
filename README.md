# Company Solicitation 

# AI-Powered B2B Outreach & OSINT Agent

An end-to-end automated Python agent designed for intelligent B2B prospecting. It combines Open Source Intelligence (OSINT), web scraping, and Large Language Models (LLMs) to identify key corporate contacts, construct their email addresses, analyze their company's context, and draft highly personalized outreach emails directly into a Gmail account.

*Built to scale corporate sponsorship research (e.g., Cartel des Mines).*

## Overview

Cold emailing often forces a trade-off between volume and personalization. This agent solves this by automating the research phase while using AI to maintain a hyper-personalized, context-aware approach. 

Instead of sending generic templates, the agent reads the target company's actual website and adapts the outreach pitch to match their core values and recent news.

## Architecture (The Pipeline)

The system is built with a modular architecture, operating in two main phases:

### Phase 1: OSINT & Contact Discovery
1. **Search (`search.py`)**: Uses the **Tavily API** to scour the web and LinkedIn to find the person currently holding a specific role (e.g., "Directeur des Ressources Humaines").
2. **Extraction (`extractor.py`)**: Passes the messy search results to **Gemini (Google AI)** to logically deduce the correct contact and extract a clean JSON `{"first_name": "...", "last_name": "..."}`.
3. **Enrichment (`enrichment.py`)**: Queries the **Hunter.io API** to find the target company's email pattern (e.g., `{first}.{last}@domain.com`) and constructs the final email address.

### Phase 2: Contextualization & Delivery
4. **Scraping (`scraper.py`)**: Uses the **Firecrawl API** to extract the main content of the company's website and converts it into clean Markdown.
5. **Generation (`generator.py`)**: Feeds the Markdown data and a base template to **Gemini**. The LLM acts as an expert copywriter, subtly modifying the template to align with the company's DNA.
6. **Delivery (`gmail_draft.py`)**: Uses **OAuth 2.0 and the Gmail API** to securely create a draft in the user's inbox, ready for human review before sending.

## Setup & Installation

**1. Clone the repository**
```bash
git clone [https://github.com/your-username/ai-sponsorship-agent.git](https://github.com/your-username/ai-sponsorship-agent.git)
cd ai-sponsorship-agent

**2. Create a virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

**3. Install dependencies**
```bash
pip install -r requirements.txt

**4. Google Cloud Console Setup (OAuth)**
To allow the script to create drafts in your Gmail:
Go to the Google Cloud Console.
Enable the Gmail API.
Configure the OAuth Consent Screen (add your email as a Test User).
Create OAuth 2.0 Client ID credentials (Desktop Application).
Download the JSON file, rename it to credentials.json, and place it in the root folder of this project.

## Setup & Installation
Create a .env file at the root of the project with the following API keys. Never commit this file to version control.
Extrait de code
# .env
FIRECRAWL_API_KEY=your_firecrawl_api_key
GEMINI_API_KEY=your_gemini_api_key
HUNTER_API_KEY=your_hunter_api_key
TAVILY_API_KEY=your_tavily_api_key


Run the agent via the Command Line Interface (CLI) by providing the company name, domain, URL, and the target role.

```bash
python main.py "Decathlon" "decathlon.fr" "[https://www.decathlon.fr](https://www.decathlon.fr)" --role "Directeur des Ressources Humaines" --template rh

**CLI Arguments**
company_name: The name of the company (e.g., "Decathlon").
domain: The email domain for Hunter.io (e.g., "decathlon.fr").
url: The website URL to scrape for context (e.g., "https://www.decathlon.fr").
--role: (Optional) The specific role to look for. Default is Directeur des Ressources Humaines.
--template: (Optional) The base email template to use (generic, rh, rse, alumni).

Expected Output:
The terminal will display the OSINT progression, output the identified contact and constructed email, display the drafted text, and confirm the creation of the draft in your Gmail account.

**Disclaimer & Ethics**
This tool is designed for B2B research and contextualized outreach. It creates drafts and does not automatically send emails. Users are responsible for reviewing drafts, ensuring compliance with local data privacy laws (like GDPR in Europe), and respecting the time of the recipients.

Developed by Hugo Kuitchoua.