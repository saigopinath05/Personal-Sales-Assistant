import openai
import pinecone

from app.helpers import create_query_with_pinecone_context

OPENAI_API_KEY="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"
PINECONE_API_KEY="9e4aff7f-7140-4d88-a5ba-f66328f2d0ce"
PINECONE_API_ENV="us-west1-gcp-free"

openai.api_key = OPENAI_API_KEY
query = "What's a nice looking women's shoe that's versatile for multiple activites?"
augmented_query, url, image, price = create_query_with_pinecone_context(
    "websites", "nike", query, PINECONE_API_KEY, PINECONE_API_ENV, OPENAI_API_KEY)
print(augmented_query)