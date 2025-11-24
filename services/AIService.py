from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from repositories.UserRepository import UserRepository
from repositories.AccountRepository import AccountRepository
from repositories.LeadRepository import LeadRepository
from repositories.OpportunityRepository import OpportunityRepository

class AIService:
    INDEX_FOLDER = "ai_storage/faiss_index"
    INDEX_NAME = "index" 

    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.llm = ChatGroq(
            temperature=0,
            model_name="llama-3.1-8b-instant",
        )

        self.vector_store = None 


    def _get_all_data_as_text(self):
        all_text_chunks = []

        users = UserRepository.get_all_users()
        for user in users:
            text = f"User Record: Name is {user.username}. Email is {user.email}."
            all_text_chunks.append(text)
        
        accounts = AccountRepository.get_all_accounts()
        for acc in accounts:
            text = (
                f"Account Record: The company '{acc.name}' operates in the '{acc.industry}' industry. "
                f"Contact Email: {acc.email_primary}, Phone: {acc.phone_primary}. "
                f"This account is managed by User ID {acc.assigned_user_id}."
            )
            all_text_chunks.append(text)
            
        leads = LeadRepository.get_all_leads()
        for lead in leads:
            text = (
                f"Lead Record: {lead.first_name + " " + lead.last_name} is a potential customer. "
                f"Status: '{lead.status}'. Source: '{lead.lead_source}'. "
                f"Contact Info: Email {lead.email_primary}, Phone {lead.phone_primary}. "
                f"Assigned to User ID {lead.assigned_user_id}."
            )
            all_text_chunks.append(text)

        opps = OpportunityRepository.get_all_opportunities()
        for opp in opps:
            text = (
                f"Opportunity Record: Deal '{opp.name}' is valued at ${opp.amount}. "
                f"It is currently in the '{opp.sales_stage}' stage with a probability of {opp.probability}%. "
                f"Expected to close on {opp.expected_closed_date}. "
                f"Managed by User ID {opp.assigned_user_id}."
            )
            all_text_chunks.append(text)

        return all_text_chunks

    def train_ai(self):
        text_chunks = self._get_all_data_as_text()

        documents = []
        for chunk in text_chunks:
            documents.append(Document(page_content=chunk))

        print(f"Vectorizing {len(documents)} documents... (This may take a moment)")

        vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embedding_model
        )

        vector_store.save_local(self.INDEX_FOLDER, self.INDEX_NAME)

        return f"Success! Trained on {len(documents)} records and saved brain to {self.INDEX_FOLDER}."

    def _load_vector_store(self):
        path_to_index = f"{self.INDEX_FOLDER}/{self.INDEX_NAME}.faiss"
        
        self.vector_store = FAISS.load_local(
            self.INDEX_FOLDER, 
            self.embedding_model,
            allow_dangerous_deserialization=True 
        )

    def ask_ai(self, user_query):
        success = self._load_vector_store()
        relevant_docs = self.vector_store.similarity_search(user_query, k=3)
        
        context_text = "\n\n".join([doc.page_content for doc in relevant_docs])

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a CRM Assistant. Answer based ONLY on the Context below. If the answer is not there, say 'I don't know'."),
            ("user", "Context:\n{context}\n\nQuestion: {question}")
        ])

        chain = prompt_template | self.llm

        response = chain.invoke({
            "context": context_text,
            "question": user_query
        })

        return [response.content]