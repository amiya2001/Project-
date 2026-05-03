from services.embedder import embedder
from services.vector_store import vector_store
from services.llm import llm_service

class QueryService:

    def search(self,query: str, top_k: int=3) -> dict:

        embeded_query=embedder.embed_text(text=query)
        vec_search=vector_store.search(query_embedding=embeded_query,top_k=top_k)
        context=""
        for i in vec_search:
            context=context+i["metadata"]["source"]+"\n"+i["content"]+"\n\n"

        result=llm_service.ask(question=query,context=context)

        return {"query": query,"answer": result, "sources":vec_search}

    
query_service=QueryService()

if __name__ == "__main__":
    result = query_service.search(
        query="What is RAG?",
        top_k=3
    )
    print(f"Answer: {result['answer']}")
    print(f"\nSources used: {len(result['sources'])}")
    for s in result['sources']:
        print(f"  → [{s['score']}] {s['metadata']['source']}")