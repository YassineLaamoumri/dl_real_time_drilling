from __future__ import annotations
import lightning as L
import torch
import torch.nn as nn


class LitModel(L.LightningModule):
    def __init__(self, net: nn.Module, lr: float = 1e-3) -> None:
        super().__init__()
        self.net = net
        self.lr = lr
        self.loss = nn.MSELoss()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)

    def training_step(self, batch, _):
        x, y = batch
        yhat = self(x)
        loss = self.loss(yhat, y)
        self.log("train_loss", loss)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.lr)



