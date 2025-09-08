from torch import nn
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"{device=}")

class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Sequential(
            nn.Linear(3, 64),
            nn.ReLU(),
            nn.Linear(64,64),
            nn.ReLU(),
            nn.Linear(64, 3)
        )

    def forward(self, x):
        x = self.linear(x)
        return x

def create_model():
    """Just to check if pytorch installation is working"""
    model = SimpleModel().to(device)
    return model

if __name__ == "__main__":
    model = create_model()
    X = torch.rand(1, 3, device=device)
    logits = model(X)
    print(f"{logits=}")
    print(model)