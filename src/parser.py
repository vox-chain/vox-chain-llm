
# from langchain_community.llms import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_mistralai import ChatMistralAI

import os
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
from pydantic import ValidationError

from .intents import TransactionIntent

# huggingfacehub_api_token = os.getenv("HHUGGINIGFACEHUB_API_TOKEN")
# llm = HuggingFaceEndpoint(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
#                               max_new_tokens=200, #remember to put it back to 200
#                               top_k=40,
#                               # do_sample=False,
#                               top_p=0.99,
#                               temperature=0.001,#remember to put it back to 0.001
#                               huggingfacehub_api_token=huggingfacehub_api_token)

llm = ChatMistralAI(
    model="mistral-large-2407",   # Options: open-mixtral-8x22b, open-mixtral-8x7b, mistral-large-2407
    max_new_tokens=200,
    temperature=0,
    max_retries=2,
)


parser = JsonOutputParser(pydantic_object=TransactionIntent)


def Intent_Maker(instruction,contacts, default_chain="1313161555"):
    """
    Extracts the intent from a given user instruction.

    This function uses a language model to parse the user instruction and extract the intent
    as a JSON object that conforms to the TransactionIntent schema.

    Args:
        instruction (str): The user instruction to extract the intent from.

    Returns:
        dict or None: The extracted intent as a dictionary if successful, otherwise None.
        :param contacts:
    """

    print("Instruction: ", instruction)
    contact_dict = {contact['name']: contact['address'] for contact in contacts}


    prompt = PromptTemplate(
        template="""
            Extract the intent from the following user instruction. 
            Do not include any unnecessary or extra information.
            It is crucial to include the transaction_type.
            If the user does not mention the chain explicitly, set the "chain" field to null.
            The output should ALWAYS be a valid JSON object that conforms to the following schema:

            {intent_schema}

            User Instruction:
            {user_instruction}

            {format_instructions}
        """,
        input_variables=["user_instruction"],
        partial_variables={"intent_schema": TransactionIntent.model_json_schema(),
                           "format_instructions": parser.get_format_instructions()},
    )


    chain = prompt | llm | parser

    try:
        result = chain.invoke({"user_instruction":instruction})
        #if no chain is provided,set it to the default
        if result.get("chain") is None:
            result["chain"] = default_chain

        # Map the 'to' field to the contact's address using the dictionary
        recipient_name = result["intent"].get("to")
        if recipient_name:
            result["who"] = recipient_name

            # Get the address directly from the contact_dict
            result["intent"]["to"] = contact_dict.get(recipient_name,
                                                      recipient_name)  # Fallback to name if not found

            if result["intent"]["to"] == recipient_name:
                print(f"Warning: Contact name '{recipient_name}' not found in provided contacts.")

        print("Extracted Intent: ", result)
        return result

    except ValidationError as e:
        print("Validation Error: ", e)
        return None


if __name__ == "__main__":
    raw_instructions = [
        "hi, could you Send 2 ETH to 0x8626f6940E2eb28930eFb4CeF49B2d1F2C9C1199",
        "Transfer 10 USDC to 0xABCDEF1234567890ABCDEF1234567890ABCDEF12",
        "Please facilitate the swap of my 50 ETH for the maximum number of USDC tokens.",
        "Wrap 0.5 ETH"
    ]
    Intent_Maker(raw_instructions[2])



