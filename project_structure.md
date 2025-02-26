```plaintext
financial_document_extraction/
│-- data/                # Directory for datasets
│   │-- raw/             # Raw unprocessed data
│   │-- processed/       # Preprocessed and cleaned data
│   │-- external/        # External data sources
│
│-- notebooks/           # Jupyter notebooks for experiments
│   │-- data_exploration.ipynb  # Initial data analysis
│   │-- model_training.ipynb    # Model development
│
│-- src/                 # Source code directory
│   │-- data_preprocessing.py   # Data cleaning & feature engineering
│   │-- train_ann.py            # ANN model for classification
│   │-- train_rnn.py            # RNN model for sequence labeling
│   │-- utils.py                # Helper functions
│
│-- models/              # Saved trained models
│   │-- ann_model.pth    # Trained ANN model
│   │-- rnn_model.pth    # Trained RNN model
│
│-- deployment/          # Deployment-related files
│   │-- api/             # API code
│   │-- docker/          # Docker files for containerization
│   │-- model_service.py # Flask/FastAPI-based model inference
│
│-- config/              # Configuration files
│   │-- config.yaml      # Model & training configurations
│
│-- tests/               # Unit and integration tests
│   │-- test_data.py     # Tests for data processing
│   │-- test_models.py   # Tests for model predictions
│
│-- logs/                # Logging directory
│-- requirements.txt     # Python dependencies
│-- README.md            # Project documentation
│-- setup.py             # Installation script
│-- .gitignore           # Ignore unnecessary files
```
