from services.embedder import embedder
from services.vector_store import vector_store
from services.llm import llm_service

class ChatService:
    def __init__(self):
        self.sessions = {}  # {session_id: [messages]}

    def chat(self, session_id: str, message: str, top_k: int = 3) -> dict:
        # Step 1 — get or create session
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        # Step 2 — search ChromaDB for context
        # embed message → search → build context string
        embedded_query=embedder.embed_text(text=message)
        vec_search=vector_store.search(query_embedding=embedded_query,top_k=top_k)
        context=""
        for i in vec_search:
            context += f"Source: {i['metadata']['source']}\n"
            context += f"Content: {i['content']}\n\n"

        

        #return {"message": message,"answer": result, "sources":vec_search}


        # Step 3 — add user message to history
        self.sessions[session_id].append(
            {"role": "user", "content": message}
        )

        # Step 4 — call llm_service.chat() with full history + context
        result=llm_service.chat(messages=self.sessions[session_id], context=context)

        # Step 5 — add Claude's response to history
        self.sessions[session_id].append(
            {"role": "assistant", "content": result}
        )

        # Step 6 — return result
        return {
            "session_id": session_id,
            "answer": result,
            "turn": len(self.sessions[session_id]) // 2
        }

    def clear_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

chat_service = ChatService()


if __name__ == "__main__":
    r1 = chat_service.chat("session_1", "What is RAG?")
    print(f"Turn 1: {r1['answer']}\n")

    r2 = chat_service.chat("session_1", "Can you explain it more simply?")
    print(f"Turn 2: {r2['answer']}\n")

    r3 = chat_service.chat("session_1", "What did I ask you first?")
    print(f"Turn 3: {r3['answer']}")