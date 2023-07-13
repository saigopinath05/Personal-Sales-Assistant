from fastapi import APIRouter, status, HTTPException
import os
from app.helpers import *
from app.constants import *

router = APIRouter()

# Takes in a query and company and answers the query using pinecone context from that company's namespace
# Parameters should NOT be in quotes when making the call
@router.get("/answer", status_code=status.HTTP_200_OK)
async def answer(query: str, company: str = "Nike") -> str:
    # Pinecone is case-sensitive so company name should be converted to lower
    namespace = company.lower()

    # Get the env constant variables
    """
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = OPENAI_API_KEY
    if not OPENAI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="OPENAI_API_KEY undefined")

    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    if not PINECONE_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="PINECONE_API_KEY undefined")

    PINECONE_API_ENV = os.getenv("PINECONE_API_ENV")
    if not PINECONE_API_ENV:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="PINECONE_API_ENV undefined")
"""
    # Set the system message
    SYSTEM_MSG = f"""You are a {company} sales representative. 
        Given the pre-determined recommended shoe data, present it to the customer, 
        explaining why the shoe fits the customer's query."""

    try:
        augmented_query, url, image, price = create_query_with_pinecone_context(
            "websites", namespace, query, PINECONE_API_KEY, PINECONE_API_ENV, OPENAI_API_KEY)
    # Just hard code the response if there isn't any matching pinecone context
    # Otherwise feeding it the original query can cause it to hallucinate
    except TypeError as e:
        return f"Hello! I am an automated {company} Sales Representative. I am designed to help you find the right shoes for your needs. Please tell me about what you're looking for so I may help you find the best shoe for you!"

    response = generate(augmented_query=augmented_query, system_msg=SYSTEM_MSG)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to connect to OpenAI server")
    response += '\n' + "price: " + price + " link: " + url + "\n" + image
    return response


