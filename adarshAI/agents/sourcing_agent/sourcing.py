def ingest_resumes():
    print("Ingest resumes: Function started")  # 🔍 Debug print
    ...
    print("✅ Ingest resumes: Function completed")


import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

# Initialize ChromaDB
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="your-collection", embedding_function=embedding_function)


# Simulate resume data
resumes = [
    {
        "id": "resume1",
        "name": "Jane Doe",
        "content": "3 years experience in ML, Python, NLP. B.Tech in CS.",
        "skills": ", ".join(["Python", "NLP", "ML"]) 
    },
    # Add more simulated resumes...
]

for resume in resumes:
    try:
        if "text" not in resume or "metadata" not in resume or "id" not in resume:
            print("Skipping invalid resume:", resume)
            continue

        metadata = resume["metadata"]

        for key, value in metadata.items():
            if isinstance(value, list):
                metadata[key] = ", ".join(map(str, value))

        collection.add(
            documents=[resume["text"]],
            metadatas=[metadata],
            ids=[resume["id"]]
        )
        print(f"✅ Successfully added: {resume['id']}")
    except Exception as e:
        print(f"❌ Error adding resume {resume.get('id', 'unknown')}: {e}")
