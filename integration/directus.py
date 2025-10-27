from config.settings import DIRECTUS_API_URL, DIRECTUS_STATIC_TOKEN
from logging_config import logger
import requests


class Directus:
    def __init__(self):
        self.url = DIRECTUS_API_URL
        self.headers = {"Authorization": f"Bearer {DIRECTUS_STATIC_TOKEN}"}

    def get(self, collection: str, params: dict = None):
        """Busca por items no directus e retorna um array de items."""
        try:
            response = requests.get(
                f"{self.url}/{collection}",
                headers=self.headers,
                params=params,
                timeout=300,
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"  ❌ Erro ao buscar collection '{collection}': {str(e)}")
            raise

    def uploadFiles(self, buffers: list):
        """Faz upload de múltiplos arquivos para Directus em uma única requisição."""
        files = [
            ("file[]", (item["nome"], item["buffer"], "application/octet-stream"))
            for item in buffers
        ]

        try:
            response = requests.post(
                f"{self.url}/files", headers=self.headers, files=files, timeout=300
            )
            response.raise_for_status()

            file_ids = [item["id"] for item in response.json()["data"]]
            return file_ids

        except requests.exceptions.RequestException as e:
            logger.error(f"  ❌ Erro no upload para Directus: {str(e)}")
            raise
