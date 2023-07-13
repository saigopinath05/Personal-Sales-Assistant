import openai
import pinecone

def create_query_with_pinecone_context(index_name, namespace, query, pinecone_api_key, pinecone_api_env, openai_api_key):
    openai.api_key = openai_api_key
    embed_query = openai.Embedding.create(
        input=query,
        engine="text-embedding-ada-002"
    )
    query_embeds = embed_query['data'][0]['embedding']

    # Initialize connection to Pinecone
    pinecone.init(api_key=pinecone_api_key, environment=pinecone_api_env)
    index = pinecone.Index(index_name)

    # Get top matching result from pinecone along with the metadata (text, title, image, url, price)
    response = index.query(query_embeds, top_k=1, include_metadata=True, namespace=namespace)

    if not response or len(response['matches']) == 0:
        print("No context found")
        return None

    # Get all metadata
    contexts = [item['metadata']['text'] for item in response['matches']][0]
    title = [item['metadata']['title'] for item in response['matches']][0]
    image = [item['metadata']['images'] for item in response['matches']][0]
    url = [item['metadata']['url'] for item in response['matches']][0]
    price = [item['metadata']['price'] for item in response['matches']][0]

    # Combine the original query with the text context and the name of the product
    augmented_query = f"""
    CONTEXT: {contexts}
    PRODUCT TITLE: {title}
    PRICE: {price}
"""
    augmented_query = augmented_query + query

    # Return the augmented query with the metadata we want to present to the user
    return augmented_query, url, image, price


# Helper function to generate from pinecone context using OpenAI
def generate_openai(augmented_query, system_msg):
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": augmented_query}
        ]
    )
    result = chat['choices'][0]['message']['content']
    return result


# Calls generate_openai, trying several times since sometimes their server is briefly down
def generate(augmented_query, system_msg):
    succeeded = False
    for i in range(100):
        try:
            response = generate_openai(augmented_query, system_msg)
        except:
            continue
        else:
            succeeded = True
            break
    if not succeeded:
        return None
    return response