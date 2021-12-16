import torch
import torch.nn as nn
import torch.nn.functional as F

from nets import Encoder, Decoder
from activations import BinaryConcrete

class StateAE(nn.Module):
    def __init__(self, parameters, device):
        super().__init__()
        self.encoder = Encoder(parameters)
        self.activation = BinaryConcrete(device=device, total_epochs=parameters["epochs"])
        self.decoder = Decoder(parameters)
    
    def forward(self, x, epoch):
        out = {"input": x}
        out["encoded"] = self.encoder(out["input"])
        out["discrete"] = self.activation(out["encoded"], epoch)
        out["decoded"] = self.decoder(out["discrete"])
        return out