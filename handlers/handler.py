from services.handler_processor import MessageProcessor
from logging_config import logger
import traceback
import json


def process_message(ch, method, properties, body):
    try:
        logger.info("Iniciando Processamento")

        data = json.loads(body.decode("utf-8"))

        processor = MessageProcessor(data)
        processor.process_data()

        ch.basic_ack(delivery_tag=method.delivery_tag)

        logger.info("Processamento Concluido")

    except Exception as e:
        logger.critical(f"Erro ao processar: {e} {traceback.format_exc()}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
