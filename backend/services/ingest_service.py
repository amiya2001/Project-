from chunker import chunker
from embedder import embedder
from vector_store import vector_store




class IngestService:



    def ingest_document(self,filename: str, content: str, tags: list[str]=[]) -> dict:
        
        
        try:
            chunks=chunker.chunk_text(content,metadata={"source": filename,"tags":str(tags)})
            count=0
            for chunk in chunks:
                
                chunk_id=f"{filename}_chunk_{chunk['metadata']['chunk_index']}"
                embedding=embedder.embed_text(chunk["text"])
                vector_store.add_document(id=chunk_id,text=chunk["text"],embedding=embedding,metadata=chunk["metadata"])
                count+=1

            return {"filename": filename,"status": "success","chunks_created": count}

        except Exception as e:
            return {"filename": filename,"status": "error","error": str(e)}
        
      
ingest_service = IngestService()


if __name__ == "__main__":
    result = ingest_service.ingest_document(
        filename="test.txt",
        content="""
        Retrieval Augmented Generation (RAG) is a technique that combines
        information retrieval with text generation. Instead of relying solely
        on a language model's parametric knowledge, RAG retrieves relevant
        documents from an external knowledge base and uses them to augment
        the generation process. This allows the model to access up-to-date
        information and produce more accurate, grounded responses.
        """ * 5,
        tags=["AI", "RAG"]
    )
    print(result)
