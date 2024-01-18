from datetime import datetime
from rag import logger
import logging


logger.setup_logger()
log = logging.getLogger(__name__)


# Function to generate a unique ID
def generate_id() -> str:
    return str(datetime.now().timestamp()).replace('.', '')
