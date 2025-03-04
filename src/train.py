# train.py- Train the Model


import torch  # PyTorch library
from torch.utils.data import DataLoader  # For batch loading
from transformers import AdamW  # Optimizer for fine-tuning
from dataset import InvoiceDataset  # Custom dataset class
from model import InvoiceModel  # LayoutLMv3 model
import config  # Import training configurations

# Load dataset (train directory)
train_dataset = InvoiceDataset(config.TRAIN_DIR)

# DataLoader for batching
train_loader = DataLoader(train_dataset, batch_size=config.BATCH_SIZE, shuffle=True)

# Initialize the model with the correct number of labels
model = InvoiceModel(config.NUM_LABELS)

# Set device to GPU if available, otherwise use CPU
device = torch.device(config.DEVICE if torch.cuda.is_available() else "cpu")
model.to(device)  # Move model to the selected device

# Define optimizer (AdamW is commonly used for Transformers)
optimizer = AdamW(model.parameters(), lr=config.LEARNING_RATE)

# Training loop
for epoch in range(config.NUM_EPOCHS):  # Loop through epochs
    model.train()  # Set model to training mode
    total_loss = 0  # Track total loss

    for batch in train_loader:  # Loop through dataset in batches
        pixel_values = batch["pixel_values"].to(device)  # Move image data to device
        bbox = batch["bbox"].to(device)  # Move bounding boxes to device
        labels = batch["labels"].to(device)  # Move labels to device

        optimizer.zero_grad()  # Reset gradients
        outputs = model(pixel_values=pixel_values, bbox=bbox, labels=labels)  # Forward pass
        loss = outputs.loss  # Compute loss
        loss.backward()  # Backpropagation
        optimizer.step()  # Update model weights

        total_loss += loss.item()  # Track total loss

    print(f"Epoch {epoch + 1}, Loss: {total_loss / len(train_loader)}")  # Print epoch loss

# Save the trained model
torch.save(model.state_dict(), "layoutlmv3_invoice.pth")
print("Model saved successfully!")  # Confirmation message
# The training script loads the dataset, initializes the model, optimizer, and device, and then runs the training loop for the specified number of epochs. The model is saved after training is complete.