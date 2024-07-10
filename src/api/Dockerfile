# Use an official Python runtime as a parent image
FROM nvidia/cuda:12.5.0-base-ubuntu22.04

# Set the working directory in the container
WORKDIR /app

# Install CMake and other necessary tools
RUN apt-get update && \
    apt-get install -y cmake g++ python3 pip nvidia-cuda-toolkit && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables
ENV HOST=0.0.0.0
ENV PORT=8000
#ENV CONFIG_FILE=config.json

# Run uvicorn server
CMD ["python3", "-m", "llama_cpp.server", "--n_gpu_layers", "-1"]
