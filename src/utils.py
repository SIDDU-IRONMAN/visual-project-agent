import logging
import sys

# Standardized logging configuration
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

# Custom Exceptions for robust error handling
class AgentError(Exception):
    """Base exception for the Visual Product Agent."""
    pass

class VisionError(AgentError):
    """Raised when an error occurs during the vision identification phase."""
    pass

class ResearchError(AgentError):
    """Raised when an error occurs during the web research phase."""
    pass

class SynthesisError(AgentError):
    """Raised when an error occurs during the data synthesis phase."""
    pass
