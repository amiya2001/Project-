from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self):
        
        self.model=SentenceTransformer("all-MiniLM-L6-v2")


    def embed_text(self,text: str) -> list[float]:
        embedding=self.model.encode(text)
        return embedding.tolist()


    def embed_batch(self,texts: list[str]) -> list[list[float]]:
        batch_embedding=self.model.encode(texts)
        return batch_embedding.tolist()

embedder=Embedder()

if __name__=="__main__":
    # Test 1 — single embedding
    vec = embedder.embed_text("How does RAG work?")
    print(f"Embedding dimensions: {len(vec)}")  # should print 384
    print(f"First 5 values: {vec[:5]}")

    # Test 2 — batch
    vecs = embedder.embed_batch(["Hello world", "RAG is powerful"])
    print(f"Batch size: {len(vecs)}")  # should print 2
    print(f"Each embedding dimensions: {len(vecs[0])}")  # should print 384