from logging.handlers import RotatingFileHandler
import logging
import os

# Caminho da pasta de logs
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Configuração do logger principal
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)  # Pode ser DEBUG, INFO, WARNING, ERROR, CRITICAL

# Handler com rotação automática (5 MB, até 3 arquivos antigos)
file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,  # 5MB
    backupCount=3,
    encoding="utf-8",
)

# Formato do log
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(message)s"
)
file_handler.setFormatter(formatter)

# Adiciona o handler (evita duplicar se já configurado)
if not logger.handlers:
    logger.addHandler(file_handler)

# Logger pronto para uso
logger.info("Logger configurado com sucesso.")