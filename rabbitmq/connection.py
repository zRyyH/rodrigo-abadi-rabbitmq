from logging_config import logger
from config.settings import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_USER,
    RABBITMQ_PASSWORD,
)
import time
import pika


def get_connection(retry_delay=5):
    """
    Retorna uma conexão RabbitMQ com reconexão automática em caso de falha.

    :param retry_delay: tempo em segundos entre tentativas de reconexão
    """
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials,
        heartbeat=300,  # 60 minutos
        blocked_connection_timeout=300,  # 60 minutos
    )

    while True:
        try:
            connection = pika.BlockingConnection(parameters)
            if connection.is_open:
                logger.info("✅ Conectado ao RabbitMQ")
                return connection
        except pika.exceptions.AMQPConnectionError as e:
            logger.critical(f"❌ Erro ao conectar ao RabbitMQ: {e}")
            logger.critical(f"⚠️ Tentando reconectar em {retry_delay}s...")
            time.sleep(retry_delay)
        except Exception as e:
            logger.critical(f"❌ Erro inesperado: {e}")
            logger.critical(f"⚠️ Tentando reconectar em {retry_delay}s...")
            time.sleep(retry_delay)
