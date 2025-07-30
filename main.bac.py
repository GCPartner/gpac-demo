from vertexai.preview.language_models import TextEmbeddingModel
import vertexai
import chromadb
from chromadb.config import Settings
import functions_framework


def get_embedding(question: str, project_id: str, region: str, model: str = "textembedding-gecko@001"):
    vertexai.init(project=project_id, location=region)
    embedding_model = TextEmbeddingModel.from_pretrained(model)
    embedding = embedding_model.get_embeddings([question])

    return embedding[0].values


def get_context(embedding, collection):
    context = ""
    documents = collection.query(query_embeddings=[embedding], n_results=3)
    for document in documents['documents'][0]:
        context += f" \n{document}"
    return context


def main():
    #  TODO: Fix hardcoded stuff
    collection_name = "Google_Cloud_Platform_Podcast"
    project_id = "cody-hill-project-293913"
    region = "us-central1"
    question = "Tell me about Platform9"


    client = chromadb.HttpClient(host='localhost', port=8000)
    collection = client.get_collection(name=collection_name)
    embedding = get_embedding(question, project_id, region)
    
    context = get_context(embedding, collection)
    prompt = f"""You are a cheerful question and answer bot. You are only to use the information provided to you 
in the "CONTEXT:" below to answer questions. All of this context is from transcripts of a PodCast. 
Do not use your own knowledge to answer any questions.
CONTEXT: ```{context}```
Question: {question}
Answer:"""
    print(prompt)
    #print(call_llm(prompt))


if __name__ == "__main__":
    main()