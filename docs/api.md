# API Documentation

## Overview
This API allows users to:
- Extract intents from user input to create blockchain transactions.

## Base URL
``http://localhost:5000``

## Endpoints

### 1. Extract Intent
- **Endpoint**: `/IntentMaker`
- **Method**: `POST`
  - **Description**: Extracts intent from user input and builds a transaction based on the extracted intent.
    - **Request Body**: 
      - `application/json`
          - fields:
            - message (string): The raw text input from which the intent will be extracted.
            -contacts (array): A list of contact objects containing name and address.
      - **Example**:
        ```
        {
          "message": "Send 5 ethereum to Alice",
          "contacts": [
            {
              "name": "Mouad",
              "address": "0x71C7656EC7ab88b098defB751B7401B5f6d8976F"
            },
            {
              "name": "Alice",
              "address": "0x5A2d1F2C9C1199B9B9B4e65E92DB7A6cD0805DB9"
            }
          ]
        }
        ```
- **Response**: 
  - `200 OK` - If the intent is successfully extracted and the transaction is built.
    ```json
  {
    "intent": {
      "transaction_type": "TRANSFER",
      "amount": 5,
      "to": "0x5A2d1F2C9C1199B9B9B4e65E92DB7A6cD0805DB9"
    },
    "chain": "1313161555",
    "who": "Alice"
  }
    ```
  - `400 Bad Request` - If the intent could not be extracted.
    ```json
    {
      "message": "Invalid input or unable to extract intent."
    }
    ```
  - `500 Internal Server Error` - If an error occurs during processing.
    ```json
    {
      "message": "Failed to process request: <error details>"
    }
    ```
