import os
import base64
import logging
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

# this scope allows for creating drafts in Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

def authenticate_gmail():
    """Gère l'authentification OAuth 2.0 avec Gmail."""
    creds = None
    # the token.json file stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                logger.error("Le fichier credentials.json est introuvable. Veuillez le télécharger depuis Google Cloud Console.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return creds

def create_gmail_draft(to_email: str, subject: str, message_body: str):
    """Crée un brouillon dans la boîte Gmail de l'utilisateur authentifié."""
    creds = authenticate_gmail()
    if not creds:
        return None

    try:
        # Build the Gmail service
        service = build('gmail', 'v1', credentials=creds)

        # Create the email message
        message = EmailMessage()
        message.set_content(message_body)
        message['To'] = to_email
        message['From'] = 'me' # 'me' represents the authenticated user
        message['Subject'] = subject

        # Encode the message in base64
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'message': {'raw': encoded_message}}

        # Create the draft
        logger.info("Création du brouillon sur Gmail en cours...")
        draft = service.users().drafts().create(userId="me", body=create_message).execute()
        
        logger.info("Brouillon créé avec succès ! (Draft ID: %s)", draft['id'])
        return draft

    except HttpError as error:
        logger.error("Une erreur est survenue lors de la création du brouillon : %s", error)
        return None