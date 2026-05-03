import chromadb as cd


class VectorStore:
    

    def __init__(self):
        self.client=cd.PersistentClient(path="./chroma_db")

        self.collection=self.client.get_or_create_collection(name="knowledge",metadata={"hnsw:space": "cosine"})


    def add_document(self,id: str, text: str, embedding: list[float], metadata: dict) -> None:
        self.collection.upsert(ids=[id],
                            embeddings=[embedding],
                            documents=[text],
                            metadatas=[metadata])

    def search(self,query_embedding: list[float], top_k: int=5) -> list[dict]:
         result=self.collection.query(query_embeddings=[query_embedding],
                                      n_results=top_k)
         ids=result["ids"][0]
         documents=result["documents"][0]
         metadatas=result["metadatas"][0]
         distances=result["distances"][0]

         clean_data=[]

         for i in range(len(ids)):
             clean_data.append({"id":ids[i],
                                "content":documents[i],
                                "metadata":metadatas[i],
                                "score":round(1-distances[i],4)})
             
         return clean_data

    def get_all_documents(self)->list[dict]:
        all_data=self.collection.get(include=["documents","metadatas"])

        datas=[]
        for i in range(len(all_data["ids"])):
            datas.append({"id":all_data["ids"][i],
                          "content":all_data["documents"][i],
                          "metadata":all_data["metadatas"][i]})


        return datas


    def delete_document(self,id: list[str]) ->None:
        self.collection.delete(ids=id)


vector_store=VectorStore()

if __name__=="__main__":
    from embedder import embedder

    # Add 3 test documents
    docs = [
        ("doc_001", "RAG stands for Retrieval Augmented Generation"),
        ("doc_002", "ChromaDB is a vector database for storing embeddings"),
        ("doc_003", "FastAPI is a modern Python web framework"),
    ]

    for id, text in docs:
        embedding = embedder.embed_text(text)
        vector_store.add_document(
            id=id,
            text=text,
            embedding=embedding,
            metadata={"source": "test"}
        )
    print("✅ Documents added")

    # Search
    query = "What is retrieval augmented generation?"
    query_embedding = embedder.embed_text(query)
    results = vector_store.search(query_embedding, top_k=2)

    print(f"\n🔍 Query: {query}")
    print(results)
    for r in results:
        print(f"  → [{r['score']:.3f}] {r['content']}")

    # Get all
    all_docs = vector_store.get_all_documents()
    print(f"\n📚 Total documents stored: {len(all_docs)}")
    





