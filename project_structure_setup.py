import os

# Define project structure as a list of directories
project_structure = [
    "data/raw",
    "data/processed",
    "data/external",
    "notebooks",
    "src",
    "models",
    "deployment/api",
    "deployment/docker",
    "config",
    "tests",
    "logging_setup",
]

# Define files to create (list of file paths)
files_to_create = [
    "notebooks/data_exploration.ipynb",
    "notebooks/model_training.ipynb",
    "src/data_preprocessing.py",
    "src/train_ann.py",
    "src/train_rnn.py",
    "src/utils.py",
    "models/ann_model.pth",
    "models/rnn_model.pth",
    "deployment/model_service.py",
    "config/config.yaml",
    "tests/test_data.py",
    "tests/test_models.py",
    "requirements.txt",
    "README.md",
    "setup.py",
    ".gitignore",
]

def create_project_structure():
    """Creates directories and files for the project structure."""

    # Create directories
    for directory in project_structure:
        os.makedirs(directory, exist_ok=True)
        print(f"📂 Created directory: {directory}")

    # Create files
    for file_path in files_to_create:
        if os.path.exists(file_path):
            print(f"⚠️ File already exists: {file_path}")
        else:
            with open(file_path, "w") as f:
                f.write("")  # Create an empty file
            print(f"📄 Created file: {file_path}")

if __name__ == "__main__":
    create_project_structure()
    print("\n✅ Project structure successfully created!")