import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq  
from langchain_core.prompts import ChatPromptTemplate 
from models.User import User

class AIService:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        self.llm = ChatGroq(
            temperature=0, 
            model_name="llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.vector_store = None

    def train_with_users(self, users: list[User]):
        text_data = []
        metadatas = [] 
        
        for user in users:
            content = f"User ID: {user.id}, Username: {user.username}, Email: {user.email}"

            text_data.append(content)
            
            metadatas.append({"user_id": user.id})

        if text_data:
            self.vector_store = FAISS.from_texts(
                texts=text_data,
                embedding=self.embedding_model,
                metadatas=metadatas
            )

    def search_users(self, query: str):
        if not self.vector_store:
            return ["AI is not trained yet."]

        results = self.vector_store.similarity_search(query, k=3)
        context_data = "\n".join([doc.page_content for doc in results])

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer the user's question strictly based on the context provided below. If the answer is not in the context, say you don't know."),
            ("human", "Context:\n{context}\n\nQuestion: {question}")
        ])

        chain = prompt | self.llm

        response = chain.invoke({
            "context": context_data,
            "question": query
        })
        
        return [response.content]