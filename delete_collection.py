import chromadb

chromadb_client = chromadb.HttpClient(host="127.0.0.1", port=8000)
collections = chromadb_client.list_collections()
print(collections)
chromadb_client.delete_collection(name="Google_Cloud_Platform_Podcast")
collections = chromadb_client.list_collections()
print(collections)
