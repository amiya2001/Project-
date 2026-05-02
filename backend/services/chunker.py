#import math
class Chunker:
    
    def __init__(self,chunk_size: int=200, overlap: int=50):

        self.chunk_size=chunk_size
        self.overlap=overlap




    def chunk_text(self,text: str, metadata: dict={})-> list[dict]:
        result=[]
        self.text=text
        word_lists=self.text.split()
        chunk_index=0
        start=0
        end=self.chunk_size
        #total_chunk=math.ceil((len(word_lists)-self.overlap)/(self.chunk_size-self.overlap))
        total_words=len(word_lists)
        while start<total_words:

            sentence=" ".join(word_lists[start:end])
            result.append({"text":sentence,"metadata":{"source":metadata["source"],"chunk_index":chunk_index,"word_count":len(word_lists[start:end])}})
            start=end-self.overlap
            end=start+self.chunk_size
            chunk_index+=1

        for chunk in result:
            chunk["metadata"]["total_chunks"]=len(result)

        return result
    
chunker = Chunker()



if __name__=="__main__":
    sample = """
    Retrieval Augmented Generation (RAG) is a technique that combines
    information retrieval with text generation. Instead of relying solely
    on a language model's parametric knowledge, RAG retrieves relevant
    documents from an external knowledge base and uses them to augment
    the generation process. This allows the model to access up-to-date
    information and produce more accurate, grounded responses. The retrieval
    component typically uses dense vector search to find semantically similar
    documents. These documents are then concatenated with the user query and
    passed to the language model as context. RAG has become a standard
    approach for building knowledge-intensive NLP applications because it
    combines the flexibility of neural language models with the precision
    of information retrieval systems. The technique was introduced by
    Facebook AI Research in 2020 and has since been widely adopted in
    production systems across many industries including healthcare,
    finance, and legal services.
    """ * 3  # repeat to get enough words to chunk

    chunks = chunker.chunk_text(sample, metadata={"source": "test.txt"})

    print(f"Total chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1}:")
        print(f"  Words:   {chunk['metadata']['word_count']}")
        print(f"  Preview: {chunk['text'][:80]}...")
