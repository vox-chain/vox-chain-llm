from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from hexbytes import HexBytes

from src.parser import Intent_Maker
from src.router import transaction_router
from src.utils.signANDsend import sign_and_send_transaction

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def serialize_transaction_receipt(receipt):
    """
    Helper function to convert the AttributeDict to a JSON-serializable dictionary

    :param receipt: Transaction receipt to serialize
    :return: serialized receipt
    """

    def serialize(value):
        if isinstance(value, (list, tuple)):
            return [serialize(item) for item in value]
        elif isinstance(value, dict):
            return {key: serialize(val) for key, val in value.items()}
        elif isinstance(value, HexBytes):
            return value.hex()
        return value

    return serialize(receipt)


@app.route('/IntentMaker', methods=['POST'])
def intent_maker():
    try:
        # Parse JSON request
        request_data = request.get_json()

        if not request_data:
            logger.error("No JSON data received")
            return jsonify({"message": "No JSON data provided"}), 400

        # Extract message and contacts from request
        message = request_data.get('message')
        contacts = request_data.get('contacts', [])

        if not message:
            logger.error("No message provided in request")
            return jsonify({"message": "Message is required"}), 400

        logger.info(f"Received input - Message: {message}, Contacts: {contacts}")

        # Create a context object with both message and contacts
        context = {
            'message': message,
            'contacts': {contact['name']: contact['address'] for contact in contacts}
        }

        # Step 1: Extract the intent from user input with context
        extracted_intent = Intent_Maker(message,contacts)
        logger.info(f"Extracted Intent: {extracted_intent}")

        if extracted_intent is None:
            response = jsonify({"message": "Invalid input or unable to extract intent."})
            logger.error(f"Response: {response.json}")
            return response, 400

        # Step 2: Build the transaction based on the extracted intent
        try:
            # transaction = transaction_router(extracted_intent)
            # logger.info(f"Transaction Receipt: {transaction}")

            # Serialize the transaction receipt before sending it to the front-end
            # serialized_transaction = serialize_transaction_receipt(transaction)

            # Step 3: Return the transaction receipt as a successful response
            response = jsonify({
                "message": "Transaction built successfully",
                "intent": extracted_intent,
                # "transaction": serialized_transaction
            })
            return response, 200

        except Exception as e:
            logger.error(f"Transaction creation failed: {e}")
            response = jsonify({"message": f"Transaction creation failed: {str(e)}"})
            return response, 500

    except Exception as e:
        logger.error(f"Failed to process request: {e}")
        response = jsonify({"message": str(e)})
        return response, 500


#  create health api that returns 200
@app.route('/health', methods=['GET'])
def health():
    logger.info("Server is running!")
    response = jsonify({"message": "Server is running!"})
    return response, 200
    

if __name__ == "__main__":
    app.run(debug=True)