# Vox Chain Backend

## System Overview

The Vox Chain Backend is a system designed to take user inputs in natural language, process the input using a Large Language Model (LLM) to extract **intent**

## Prerequisites

- Docker installed on your system
- API keys and environment variables ready for any integrated services (ensure they are securely configured as environment variables)

## Docker Instructions

### Building the Docker Image

To build the Docker image, navigate to the directory containing the `Dockerfile` and run the following command:

```bash
docker build -t vox-chain-backend
```

### Building the Docker Image

```bash
docker run -p 3033:5000 \
  -e LANGCHAIN_API_KEY='your_langchain_api_key' \
  -e HHUGGINGFACEHUB_API_TOKEN='your_huggingfacehub_api_token' \
  -e MISTRAL_API_KEY='your_mistral_api_key' \
  vox-chain-backend
```

After starting the container, you can test the backend by sending requests to http://localhost:3033.
