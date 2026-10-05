# 📖 Guide d'Installation pour Débutants (Sans aucune notion de code)

Bienvenue ! Cet outil a été créé pour automatiser la prospection de partenariats. Sous le capot, c'est un programme qui utilise l'Intelligence Artificielle pour chercher des contacts, analyser des sites web et rédiger des mails personnalisés.

Même si vous n'avez jamais codé de votre vie, vous pouvez le faire fonctionner sur votre ordinateur en suivant ces étapes pas-à-pas. Prenez votre temps, lisez bien chaque ligne.

---

## Étape 1 : Installer le moteur (Python)
L'outil est écrit en Python. Votre ordinateur a besoin d'apprendre cette "langue" pour le lire.

1. Allez sur le site officiel : [python.org/downloads](https://www.python.org/downloads/)
2. Cliquez sur le bouton jaune "Download Python".
3. Lancez le fichier téléchargé.
4. ⚠️ **TRÈS IMPORTANT (Pour Windows) :** Sur la toute première fenêtre de l'installateur, tout en bas, **cochez impérativement la case "Add Python.exe to PATH"** avant de cliquer sur "Install Now". Si vous oubliez cette case, rien ne marchera.

## Étape 2 : Récupérer le projet sur votre PC
Au lieu d'utiliser des commandes compliquées, nous allons faire simple :

1. Sur la page GitHub de ce projet, cherchez le gros bouton vert **"<> Code"**.
2. Cliquez dessus, puis choisissez **"Download ZIP"**.
3. Décompressez (extrayez) ce dossier ZIP où vous le souhaitez sur votre ordinateur (par exemple dans "Documents").

## Étape 3 : Créer vos clés secrètes (API)
Notre outil utilise plusieurs services externes. Une clé API est comme un badge d'accès VIP pour utiliser ces services. Vous devez créer des comptes gratuits sur ces 4 sites et récupérer vos clés (qui ressemblent à de longues suites de lettres et de chiffres) :

1. **Tavily (Pour la recherche web) :** Allez sur [tavily.com](https://tavily.com), créez un compte, allez dans l'onglet "API Keys" et copiez votre clé.
2. **Hunter.io (Pour trouver les formats d'emails) :** Allez sur [hunter.io](https://hunter.io), créez un compte, allez dans "API" et copiez votre clé.
3. **Firecrawl (Pour lire les sites web) :** Allez sur [firecrawl.dev](https://www.firecrawl.dev), créez un compte et copiez la clé sur le tableau de bord.
4. **Google Gemini (Pour l'Intelligence Artificielle) :** Allez sur [aistudio.google.com](https://aistudio.google.com/), connectez-vous avec un compte Google, cliquez sur "Get API Key" puis "Create API Key" et copiez-la.

## Étape 4 : Ranger vos clés dans un fichier secret
Votre outil a besoin de ces clés pour fonctionner.

1. Allez dans le dossier du projet (celui que vous avez dézippé à l'Étape 2).
2. Faites un "Clic droit > Nouveau > Document texte".
3. Nommez-le `.env` (Attention, juste `.env`, supprimez le `.txt` s'il est visible. Si Windows râle, utilisez un éditeur de texte comme le Bloc-notes, faites "Enregistrer sous", choisissez "Tous les fichiers" et tapez `.env`).
4. Ouvrez ce fichier avec le Bloc-notes et collez ceci en remplaçant par vos vraies clés (sans espaces) :

FIRECRAWL_API_KEY=collez_votre_cle_ici
GEMINI_API_KEY=collez_votre_cle_ici
HUNTER_API_KEY=collez_votre_cle_ici
TAVILY_API_KEY=collez_votre_cle_ici

5. Enregistrez et fermez.

## Étape 5 : Connecter votre compte Gmail (L'étape la plus dure)
Pour que l'outil puisse créer des brouillons directement dans votre boîte mail, il faut l'autoriser via Google Cloud.

1. Allez sur la [Google Cloud Console](https://console.cloud.google.com/) et connectez-vous.
2. Acceptez les conditions, puis en haut à gauche, cliquez sur **"Sélectionner un projet"** > **"Nouveau projet"** (nommez-le "Agent Partenariat").
3. Dans la barre de recherche en haut, tapez **"Gmail API"**, cliquez dessus, puis sur **"Activer"**.
4. Allez dans le menu de gauche (les 3 traits) > **API et services** > **Écran de consentement OAuth**.
   - Choisissez **Externe** > Créer.
   - Remplissez les noms demandés et mettez votre adresse e-mail.
   - En bas, dans **Utilisateurs tests**, cliquez sur "+ Ajouter des utilisateurs" et tapez l'adresse Gmail que vous allez utiliser pour les envois.
   - Enregistrez.
5. Toujours dans le menu de gauche, allez dans **Identifiants**.
   - Cliquez sur **"+ Créer des identifiants"** > **"ID client OAuth"**.
   - Type : **Application de bureau**. Cliquez sur Créer.
6. Une fenêtre apparaît avec un bouton **Télécharger le fichier JSON**. Cliquez dessus.
7. Prenez ce fichier téléchargé, placez-le dans le dossier de votre projet, et renommez-le très exactement **`credentials.json`**.

## Étape 6 : Lancer la machine 🚀
Tout est prêt ! 

1. Ouvrez le dossier de votre projet.
2. Dans la barre d'adresse du dossier (tout en haut, là où il y a écrit le chemin comme *C:\Utilisateurs\Documents...*), cliquez, tapez `cmd` et appuyez sur Entrée. Une fenêtre noire (le terminal) s'ouvre.
3. Tapez cette commande pour installer les outils nécessaires, et appuyez sur Entrée (cela peut prendre 1 ou 2 minutes) :
   
   pip install -r requirements.txt
   
4. Une fois terminé, vous pouvez lancer votre première recherche avec cette commande :
   
   python main.py "Decathlon" "decathlon.fr" "https://www.decathlon.fr" --role "Directeur des Ressources Humaines" --template rh
   

*Lors de la toute première exécution, une page web va s'ouvrir pour vous demander d'autoriser l'application à accéder à votre Gmail. Connectez-vous, passez l'avertissement de sécurité (cliquez sur "Paramètres avancés" puis "Accéder à l'application"), et voilà ! Votre brouillon vous attendra dans votre boîte mail.*
