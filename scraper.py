import argparse
import json
import logging
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from firecrawl import Firecrawl
from firecrawl.types import FormatOption


logger = logging.getLogger(__name__)


def load_environment(env_file: Optional[str] = None) -> None:
    """Load environment variables from .env if available."""
    if env_file:
        load_dotenv(env_file)
    else:
        load_dotenv()


def get_api_key(override_key: Optional[str] = None) -> str:
    """Return the Firecrawl API key from override or environment."""
    if override_key:
        return override_key

    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        raise RuntimeError(
            "La variable d'environnement FIRECRAWL_API_KEY est requise."
        )
    return api_key


def create_firecrawl_client(api_key: str) -> Firecrawl:
    """Instantiate the Firecrawl client."""
    return Firecrawl(api_key=api_key)


def scrape_url(
    client: Firecrawl,
    url: str,
    only_main_content: bool = True,
    formats: Optional[list[FormatOption]] = None,
) -> Dict[str, Any]:
    """Scrape a URL and return a JSON-serializable document payload."""
    if formats is None:
        formats = ["markdown"]

    document = client.scrape(
        url,
        only_main_content=only_main_content,
        formats=formats,
    )

    if hasattr(document, "model_dump"):
        payload = document.model_dump(exclude_none=True)
    else:
        payload = getattr(document, "dict", lambda **kwargs: {})(exclude_none=True)

    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scraper Firecrawl pour extraire une page web et afficher les résultats JSON."
    )
    parser.add_argument("url", help="URL à scraper")
    parser.add_argument(
        "--api-key",
        help="Clé API Firecrawl (remplace FIRECRAWL_API_KEY)",
        default=None,
    )
    parser.add_argument(
        "--env-file",
        help="Chemin vers un fichier .env contenant FIRECRAWL_API_KEY",
        default=None,
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Fichier de sortie JSON. Par défaut, affiche sur stdout.",
        default=None,
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Inclure l'ensemble du contenu de la page au lieu du contenu principal uniquement.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Activer les logs de debug.",
    )
    return parser.parse_args()


def configure_logging(debug: bool = False) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s")


def main() -> int:
    args = parse_args()
    configure_logging(args.debug)

    try:
        load_environment(args.env_file)
        api_key = get_api_key(args.api_key)
        client = create_firecrawl_client(api_key)

        logger.info("Scraping %s", args.url)
        document_data = scrape_url(
            client,
            args.url,
            only_main_content=not args.full,
        )

        output = json.dumps(document_data, indent=2, ensure_ascii=False)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as handler:
                handler.write(output)
            logger.info("Résultat enregistré dans %s", args.output)
        else:
            print(output)

        return 0
    except Exception as exc:
        logger.error("Échec du scraping : %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
