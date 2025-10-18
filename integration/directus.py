from config.settings import DIRECTUS_API_URL, DIRECTUS_STATIC_TOKEN
from logging_config import logger
import requests
import json


class Directus:
    def __init__(self):
        self.url = DIRECTUS_API_URL
        self.headers = {"Authorization": f"Bearer {DIRECTUS_STATIC_TOKEN}"}

    def uploadFiles(self, buffers: list):
        """Faz upload de múltiplos arquivos para Directus em uma única requisição."""
        files = [
            ("file[]", (item["nome"], item["buffer"], "application/octet-stream"))
            for item in buffers
        ]

        response = requests.post(
            f"{self.url}/files", headers=self.headers, files=files, timeout=300
        )
        response.raise_for_status()

        return [item["id"] for item in response.json()["data"]]

    def get(self, collection: str, params: dict = None):
        """Busca por items no directus e retorna um array de items."""
        response = requests.get(
            f"{self.url}/{collection}", headers=self.headers, params=params, timeout=300
        )
        response.raise_for_status()
        return response.json()

    def create(self, collection: str, data: dict | list):
        """
        Cria um ou múltiplos registros em uma coleção do Directus.

        :param collection: nome da coleção no Directus
        :param data: dicionário (para um item) ou lista de dicionários (para múltiplos)
        :return: resposta JSON do Directus
        """
        try:
            response = requests.post(
                f"{self.url}/items/{collection}",
                headers={**self.headers, "Content-Type": "application/json"},
                json=data,
                timeout=300,
            )

            # Verifica se ocorreu tudo certo com a requisicao, caso contrario sobe um erro.
            response.raise_for_status()

            # Retorna body JSON dict
            return response.json()

        except:
            j = json.dumps(response.json(), indent=4)
            logger.critical(f"{j}")

    def update(self, collection: str, data: list):
        try:
            response = requests.patch(
                f"{self.url}/items/{collection}",
                headers={**self.headers, "Content-Type": "application/json"},
                json=data,
                timeout=300,
            )

            # Verifica se ocorreu tudo certo com a requisicao, caso contrario sobe um erro.
            response.raise_for_status()

            # Retorna body JSON dict
            return response.json()

        except:
            j = json.dumps(response.json(), indent=4)
            logger.critical(f"{j}")
