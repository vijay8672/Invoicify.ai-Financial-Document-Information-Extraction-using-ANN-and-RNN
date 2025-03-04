## model.py - Define LayoutLMv3 Model


# model.py

import torch  # PyTorch library
import torch.nn as nn  # Neural network layers
from transformers import LayoutLMv3ForTokenClassification  # Pretrained LayoutLMv3 model

class InvoiceModel(nn.Module):
    """
    Defines the LayoutLMv3 model for document processing.
    """

    def __init__(self, num_labels):
        """
        Initializes the model.
        :param num_labels: Number of entity labels to classify.
        """
        super(InvoiceModel, self).__init__()
        # Load LayoutLMv3 with the specified number of labels
        self.model = LayoutLMv3ForTokenClassification.from_pretrained(
            "microsoft/layoutlmv3-base", num_labels=num_labels
        )

    def forward(self, pixel_values, bbox, labels=None):
        """
        Forward pass through the model.
        :param pixel_values: Image tensor
        :param bbox: Bounding box coordinates
        :param labels: Target labels for training
        :return: Model output (loss during training, logits during inference)
        """
        return self.model(pixel_values=pixel_values, bbox=bbox, labels=labels)
