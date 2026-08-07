import argparse
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM

from langchain_core.prompts import ChatPromptTemplate
import os
from langchain_huggingface import HuggingFaceEndpoint
from fastapi import FastAPI

load_dotenv()

CHROMA_PATH = "chroma"
prompt_template = """
You are a customer service assistant for Maahra, a hand-embroidered ethnic wear brand. be polite and helpful.

IMPORTANT RULES:
- Answer ONLY using information  stated in the Context below
- If the answer is NOT in the Context, say "I don't have that information. Please contact us at maahra@email.com"
- Do NOT make up prices, times, or any specific details
- Do NOT use your own knowledge — only use the Context

Context:
{content}

if costumer refers previous char, use previous converstaion history

Previous Conversation:
{history}

Customer: {query}
Bot:"""





embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db=Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)




from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama3-8b-8192",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)
def get_response(query, chat_history):
    results=db.similarity_search_with_relevance_scores(query, 3)
    


    
    content='\n\n---\n\n'.join([doc.page_content for doc, _score in results])

    print(results[0][1])
    template=ChatPromptTemplate.from_template(prompt_template)
    
    

    history_text = '\n'.join([
        f"Customer: {q}\nBot: {a}" 
        for q, a in chat_history[-5:]
    ])

    prompt=template.format(content=content, history=history_text,query=query)
    print(prompt)

    response=llm.invoke(prompt)
    sources=[doc.metadata.get("source", 'unknown') for doc, _score in results]
  
    return response
if __name__ == "__main__":
    chat_history = []
    print("Maahra Customer Service Bot (type 'quit' to exit)\n")
    while True:
        query_text = input("You: ")
        if query_text.lower() == "quit":
            break
        response = get_response(query_text, chat_history)
        print(f"\nBot: {response}\n")
        chat_history.append((query_text, response))
        

    


