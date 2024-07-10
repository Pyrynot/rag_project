#!/bin/bash

# Path to the virtual environment
VENV_PATH="/home/poromies/.env"

# Path to the destination directory
DEST_DIR="/home/poromies/models"

# Model information
MODEL_NAME="bartowski/New-Dawn-Llama-3-70B-32K-v1.0-GGUF"
INCLUDE_FILE="New-Dawn-Llama-3-70B-32K-v1.0-Q4_K_M.gguf"

# Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# Create destination directory if it doesn't exist
echo "Creating destination directory if it does not exist..."
mkdir -p "$DEST_DIR"

# Download the model
echo "Downloading model from Hugging Face..."
huggingface-cli download "$MODEL_NAME" --include "$INCLUDE_FILE" --local-dir "$DEST_DIR"

# Check if the download was successful
if [ $? -eq 0 ]; then
  echo "Model downloaded successfully to $DEST_DIR"
else
  echo "Model download failed"
fi

# Deactivate the virtual environment
echo "Deactivating virtual environment..."
deactivate
