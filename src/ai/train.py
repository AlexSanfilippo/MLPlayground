import torch
from model import SimpleModel
import torch.optim as optim
import logging
from random import random
from tqdm import tqdm

class PhysicsInterface:
    
    @classmethod
    def get_model_input(device):
        return torch.rand(1, 3)

    @classmethod
    def send_model_output(device):
        return torch.rand(1, 3)


class Trainer:
    def __init__(self, model=SimpleModel, physics_interface=PhysicsInterface):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = model().to(self.device)
        self.physics_interface = physics_interface


    def train(self, loops=500, lr=0.001):
        loss_fn = torch.nn.MSELoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        for epoch in tqdm(range(loops)):
            # Forward pass
            outputs = self.model(self.physics_interface.get_model_input())
            loss = loss_fn(outputs, self.physics_interface.send_model_output())
            # optimizer
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    trainer = Trainer(SimpleModel, PhysicsInterface)
    trainer.train()