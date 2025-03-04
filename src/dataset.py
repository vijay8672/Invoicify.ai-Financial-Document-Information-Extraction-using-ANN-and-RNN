# dataset.py   ## Load and Preprocess Dataset

import os  # For handling file paths
import torch  # PyTorch library
from PIL import Image  # Image handling
from torch.utils.data import Dataset  # PyTorch Dataset class
from transformers import AutoProcessor  # Pretrained LayoutLMv3 processor

class InvoiceDataset(Dataset):
    """
    Custom PyTorch Dataset class to load images, bounding boxes, and entity labels.
    """

    def __init__(self, root_dir):
        """
        Initializes the dataset by setting paths and loading the processor.
        :param root_dir: Path to the dataset (e.g., 'train' or 'test' directory).
        """
        self.root_dir = root_dir
        self.image_files = sorted(os.listdir(os.path.join(root_dir, "img")))  # List of image files
        self.box_files = sorted(os.listdir(os.path.join(root_dir, "box")))  # List of bounding box files
        self.entity_files = sorted(os.listdir(os.path.join(root_dir, "entities")))  # List of label files

        # Load the LayoutLMv3 processor for tokenizing text and images
        self.processor = AutoProcessor.from_pretrained("microsoft/layoutlmv3-base")

    def __len__(self):
        """
        Returns the total number of samples in the dataset.
        """
        return min(len(self.image_files), 50)  # Limit to 50 records for local training

    def __getitem__(self, idx):
        """
        Returns one sample from the dataset, including the image, bounding boxes, and labels.
        :param idx: Index of the sample.
        """
        # Get file paths for image, bounding boxes, and entity labels
        img_path = os.path.join(self.root_dir, "img", self.image_files[idx])
        box_path = os.path.join(self.root_dir, "box", self.box_files[idx])
        entity_path = os.path.join(self.root_dir, "entities", self.entity_files[idx])

        # Load the image and convert it to RGB format
        image = Image.open(img_path).convert("RGB")

        # Load bounding boxes from the text file
        with open(box_path, "r") as f:
            boxes = [list(map(int, line.strip().split()[:8])) for line in f.readlines()]

        # Load entity labels from the JSON file
        with open(entity_path, "r") as f:
            labels = eval(f.read())  # Convert string to dictionary

        # Tokenize image and bounding box data using the processor
        encoding = self.processor(image, boxes=boxes, return_tensors="pt")

        return {
            "pixel_values": encoding["pixel_values"].squeeze(0),  # Image tensors
            "bbox": torch.tensor(boxes, dtype=torch.long),  # Bounding box coordinates
            "labels": torch.tensor([0] * len(boxes), dtype=torch.long),  # Dummy labels (adjust later)
        }
