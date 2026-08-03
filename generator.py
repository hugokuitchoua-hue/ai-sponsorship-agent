import os
import logging
from typing import Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

# Storing the Cartel des Mines templates
EMAIL_TEMPLATES = {
    "generic": """
Objet : Partenariat - Cartel des Mines 2027
Bonjour {{prenom}} {{nom}},
Je m’appelle Hugo Kuitchoua, élève de IMT Nord Europe, en charge des partenariats pour le Cartel des Mines 2027. Créé en 1961, le Cartel est l’un des plus grands rassemblements étudiants des écoles d’ingénieurs en France, réunissant chaque année plusieurs milliers d’étudiants européens autour d’une compétition sportive et festive. Véritable symbole de cohésion, de dépassement de soi et d’engagement collectif, cet événement emblématique constitue un temps fort de la vie étudiante. En 2027, sa 52ᵉ édition fera son retour à IMT Nord Europe et mobilisera l’ensemble de l’école pour offrir une expérience innovante, riche en émotions, mettant à l’honneur l’esprit d’accueil et la chaleur humaine du Nord.
Je vous propose un premier échange afin d’étudier comment notre événement pourrait répondre concrètement aux enjeux de votre entreprise. Qu'il s'agisse d'enjeux de recrutement, de besoins de visibilité auprès des étudiants ou de la volonté de soutenir un projet responsable et engagé, nous sommes prêts à vous aider.
Pourriez-vous me consacrer quelques minutes d’échange ou m’indiquer la personne responsable des partenariats ou des relations écoles à qui je pourrais présenter notre démarche ?
Je reste à votre disposition pour toute information complémentaire.
Cordialement,
Hugo Kuitchoua 
Membre de l’équipe Partenariat - Cartel des Mines 2027 
Mail : hugokuitchoua@gmail.com
Tél : 07 49 69 18 17
Matej Loppe 
Chef d’équipe Partenariat - Cartel des Mines 2027 
Mail : matysekloppe@gmail.com
Tél : 06 29 35 54 08

Romain Dalençon 
Responsable Communication et Partenariat - Cartel des Mines 2027 
Mail : romaindalencon003@gmail.com 
Tél : 07 82 20 05 56
""",
    "alumni": """
Objet : Partenariat – Cartel des Mines 2027
Bonjour {{prenom}} {{nom}},
Je me permets de vous contacter car vous êtes alumni de l’école. Je m’appelle Hugo Kuitchoua, actuellement étudiant à IMT Nord Europe et membre de l’équipe / chef d’équipe partenariat pour le Cartel des Mines 2027. Créé en 1961, le Cartel est l’un des plus grands rassemblements étudiants des écoles d’ingénieurs en France, réunissant chaque année plusieurs milliers d’étudiants européens autour d’une compétition sportive et festive. Véritable symbole de cohésion, de dépassement de soi et d’engagement collectif, cet événement emblématique constitue un temps fort de la vie étudiante. En 2027, sa 52ᵉ édition fera son retour à IMT Nord Europe et mobilisera l’ensemble de l’école pour offrir une expérience innovante, riche en émotions, mettant à l’honneur l’esprit d’accueil et la chaleur humaine du Nord.
Je vous propose un premier échange afin d’étudier comment notre événement pourrait répondre concrètement aux enjeux de votre entreprise. Qu’il s’agisse d’enjeux de recrutement, de besoins de visibilité auprès des étudiants ou de la volonté de soutenir un projet responsable et engagé, nous sommes prêts à vous aider.
En tant qu’ancien·ne de l’école, vous êtes notre meilleur·e ambassadeur·rice. Pourriez-vous me consacrer quelques minutes pour échanger, ou m’indiquer la personne responsable des partenariats ou des relations écoles à qui je pourrais présenter notre démarche ?
Je reste à votre disposition pour toute information complémentaire.
Cordialement,
Hugo Kuitchoua
Membre de l’équipe Partenariat - Cartel des Mines 2027
Mail : hugokuitchoua@gmail.com
Tél : 07 49 69 18 17
Matej Loppe 
Chef d’équipe Partenariat – Cartel des Mines 2027 
Mail : matysekloppe@gmail.com
Tél : 06 29 35 54 08
Romain Dalençon 
Responsable Communication et Partenariat – Cartel des Mines 2027 
Mail : romaindalencon003@gmail.com 
Tél : 07 82 20 05 56
"""
}

def generate_sponsorship_email(company_name: str, website_content: str, template_type: str, contact_name: str = None) -> Optional[str]:
    """
    Adapts a specific template for a given company
    using scraped data, without altering the core factual information.
    """
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        logger.error("The GEMINI_API_KEY is missing from the .env file.")
        return None

    if template_type not in EMAIL_TEMPLATES:
        logger.error("Invalid template type. Choose from: %s", list(EMAIL_TEMPLATES.keys()))
        return None

    base_template = EMAIL_TEMPLATES[template_type]
    client = genai.Client(api_key=api_key)

    # 1. System Prompt: The AI acts as a smart editor
    system_instruction = (
        "You are an expert in public relations working for the Cartel des Mines 2027 at IMT Nord Europe. "
        "Your task is to take a base email template and subtly modify it to perfectly fit the target company, "
        "based on their website data. The email MUST remain in French."
    )

    greeting_rule = f"Commence obligatoirement l'e-mail par 'Bonjour {contact_name},'" if contact_name else "Commence l'e-mail par 'Bonjour,'."

    # 2. User Prompt: Very strict rules to prevent hallucinating event details
    prompt = f"""
    Target Company: {company_name}
    
    Company Website Data (Markdown):
    ---
    {website_content[:4000]}
    ---
    
    Base Email Template:
    ---
    {base_template}
    ---
    INSTRUCTIONS:
    {greeting_rule}
    1. Rewrite the template to smoothly integrate a personalized hook (mentioning a recent project, value, or news from the company data) to show we did our research.
    2. Adapt the value proposition slightly to align with the company's specific context (e.g., if targeting RH, align with their hiring culture; if RSE, align with their ecological/inclusion goals).
    3. CRITICAL: DO NOT change any factual data about the event (IMT Nord Europe, 1961, Cartel des Mines 2027, 2000 students, Douai, April 22-25, Matej Loppe, Romain Dalençon).
    4. CRITICAL: Leave all bracketed variables exactly as they are (e.g., [Votre Prénom] [Votre Nom], [Nom de l'interlocuteur]) so they can be filled automatically later by a mailing tool.
    5. Output ONLY the final email text, starting with the "Objet:". Do not add any introductory or concluding commentary.
    """

    try:
        logger.info("Adapting '%s' template for %s...", template_type, company_name)
        
        # Call the Gemini API (using the model we verified earlier)
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite', # Adjust if you used a different alias from check_models.py
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.4, # Lowered to 0.5 to keep it closer to the template
            )
        )
        return response.text.strip()

    except Exception as exc:
        logger.error("AI adaptation failed: %s", exc)
        return None