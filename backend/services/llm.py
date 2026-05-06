import anthropic
from core.config import settings

class LLMService:
    def __init__(self):
        self.client=anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    def ask(self,question: str, context:str) -> str:
        system_prompt="""You are a helpful AI assistant for a Personal Knowledge System.
Answer the user's question based ONLY on the provided context.
If the answer cannot be found in the context, say:
"I don't have enough information in my knowledge base to answer this."
Be concise, accurate, and cite which source your answer comes from."""

        user = f"Context:\n{context}\n\nQuestion: {question}" 

        response=self.client.messages.create(model="claude-haiku-4-5",
                                             max_tokens=1024,
                                             system=system_prompt,
                                             messages=[{"role": "user", "content": user}])
        return response.content[0].text
    
    def chat(self,messages: list[dict], context:str="")-> str:


         # Context goes in system prompt so Claude has it throughout conversation
        system_prompt = f"""You are a helpful AI assistant for a Personal Knowledge System.
    Answer the user's question based ONLY on the provided context below.
    If the answer cannot be found in the context, 
    say:"I don't have enough information in my knowledge base to answer this.
    "Be concise, accurate, and cite which source your answer comes from.
    
    context:{context}"""

        response = self.client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            system=system_prompt,
            messages=messages   
        )
        return response.content[0].text
    
llm_service = LLMService()


if __name__ == "__main__":
    answer = llm_service.ask(
        question="What is RAG?",
        context="Source: paper.pdf\nContent: RAG stands for Retrieval Augmented Generation. It combines information retrieval with text generation to produce grounded responses."
    )
    print(answer)