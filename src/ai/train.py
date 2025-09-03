import torch
from ai.model import ExampleModel
import logging

logger = logging.getLogger(__name__)


def create_model():
    """Just to check if pytorch installation is working"""
    device = (
        torch.accelerator.current_accelerator().type
        if torch.accelerator.is_available()
        else "cpu"
    )
    logger.info(f"Using {device} device")
    model = ExampleModel().to(device)
    logger.info(model)
