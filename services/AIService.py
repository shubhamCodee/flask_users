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
            model_name="llama-3.3-70b-versatile",
        )

        self.vector_store = None 

    def _get_user_map(self):
        users = UserRepository.get_all_users()
        
        return {user.id: user.username for user in users}

    def _format_user_to_text(self, user):
        # serialization
        return f"USER RECORD: {user.username} is a system user with email {user.email}."

    def _format_lead_to_text(self, lead, user_map):
        owner_name = user_map.get(lead.assigned_user_id, "Unassigned")
        created_date = lead.created_at.strftime("%Y-%m-%d") if lead.created_at else "Unknown"
        next_followup = lead.next_followup_date.strftime("%Y-%m-%d") if lead.next_followup_date else "Not Scheduled"
        closed_date_str = lead.closed_date.strftime("%Y-%m-%d") if lead.closed_date else "N/A"

        # semantic enrichment
        identity_block = (
            f"[IDENTITY DETAILS]\n"
            f"Name: {lead.salutation or ''} {lead.first_name} {lead.last_name}\n"
            f"Designation: {lead.designation or 'N/A'} ({lead.hierarchy or 'N/A'})\n"
            f"Department: {lead.department or 'N/A'}\n"
            f"Company/Account: {lead.account_id_name or 'Independent'}\n"
            f"Industry: {lead.industry or 'General'} | Customer Type: {lead.customer_type or 'Standard'}\n"
            f"Product Interest: {lead.product_sub_category or 'General'}"
        )

        location_str = f"{lead.city or ''}, {lead.state or ''}, {lead.country or ''}"
        contact_block = (
            f"[CONTACT & LOCATION]\n"
            f"Email: {lead.email_primary} | Phone: {lead.phone_primary}\n"
            f"Website: {lead.website or 'N/A'}\n"
            f"Address: {lead.street or ''}, {lead.area or ''}, {location_str}, {lead.postal_code or ''}\n"
            f"Geofence: Lat {lead.geofence_latitude or '0'}, Lng {lead.geofence_longitude or '0'} (Radius: {lead.geofence_radius or 'N/A'})"
        )

        status_block = (
            f"[PIPELINE STATUS]\n"
            f"Current Status: {lead.status}\n"
            f"Is Converted: {'Yes' if lead.converted else 'No'}\n"
            f"Lead Source: {lead.lead_source or 'Unknown'} (Detail: {lead.other_source or '-'})"
        )
        
        if lead.lost_reason:
            status_block += f"\nLost Reason: {lead.lost_reason}"

        metrics_block = (
            f"[METRICS & TIMELINE]\n"
            f"Created On: {created_date} | Age: {lead.how_old_days or 0} Days\n"
            f"Untouched For: {lead.untouched_since_days or 0} Days\n"
            f"Next Action: {lead.next_followup_type or 'None'} on {next_followup}\n"
            f"Expected Close: {closed_date_str}"
        )

        notes_block = (
            f"[SYSTEM CONTEXT]\n"
            f"Assigned Owner: {owner_name}\n"
            f"Description: {lead.description or 'No notes provided.'}\n"
            f"Latest Comment: {lead.latest_comment or '-'}"
        )

        full_story = f"{identity_block}\n\n{contact_block}\n\n{status_block}\n\n{metrics_block}\n\n{notes_block}"
        
        return full_story

    def _format_account_to_text(self, account, user_map):
        owner_name = user_map.get(account.assigned_user_id, "Unassigned")
        
        profile_block = (
            f"[COMPANY PROFILE]\n"
            f"Account Name: {account.name}\n"
            f"Industry: {account.industry or 'General'} | Type: {account.customer_type or 'Standard'}\n"
            f"Status: {account.account_status or 'Active'} | Rating: {account.rating or 'Neutral'}\n"
            f"Website: {account.website or 'N/A'}"
        )

        location_str = f"{account.city or ''}, {account.state or ''}, {account.country or ''}"
        contact_block = (
            f"[CONTACT DETAILS]\n"
            f"Primary Email: {account.email_primary} | Phone: {account.phone_primary}\n"
            f"Secondary Emails: {account.email_json or 'None'} | Secondary Phones: {account.phone_json or 'None'}\n"
            f"Address ({account.address_type or 'Main'}): {account.street or ''}, {account.area or ''}, {location_str}, {account.postal_code or ''}\n"
            f"GSTIN: {account.gstin or 'N/A'} | PAN: {account.pan or 'N/A'}\n"
            f"Tally Migration Status: {'Migrated' if account.migrated_to_tally_branch else 'Not Migrated'}"
        )

        system_block = (
            f"[SYSTEM CONTEXT]\n"
            f"Account Owner: {owner_name}\n"
            f"Internal Team ID: {account.team_id or 'Global'}\n"
            f"Partner Team: {account.partner_user_team_id or 'N/A'} | Helpdesk Team: {account.helpdesk_user_team_id or 'N/A'}\n"
            f"Team Set ID: {account.team_set_id or 'N/A'}\n"
            f"Description: {account.description or 'No description.'}\n"
            f"Latest Comment: {account.latest_comment or '-'}"
        )

        return f"{profile_block}\n\n{contact_block}\n\n{system_block}"

    def _format_opportunity_to_text(self, opp, user_map):
        owner_name = user_map.get(opp.assigned_user_id, "Unassigned")
        close_date = opp.expected_closed_date.strftime("%Y-%m-%d") if opp.expected_closed_date else "TBD"
        actual_close = opp.closed_date.strftime("%Y-%m-%d") if opp.closed_date else "Not Closed"
        
        overview_block = (
            f"[DEAL OVERVIEW]\n"
            f"Opportunity Name: {opp.name} (ID: {opp.id})\n"
            f"Stage: '{opp.sales_stage}' (Probability: {opp.probability or 0}%)\n"
            f"Type: {opp.opportunity_type or 'New Business'} | Priority: {opp.priority or 'Medium'}\n"
            f"Lead Source: {opp.lead_source or 'Unknown'} | Customer Type: {opp.customer_type or 'Standard'}"
        )

        amount_val = opp.amount or 0
        profit_val = opp.gross_profit or 0
        commercials_block = (
            f"[COMMERCIALS]\n"
            f"Deal Value: ₹{amount_val:,.2f} | Expected Gross Profit: ₹{profit_val:,.2f}\n"
            f"Quantity: {opp.quantity or 0}\n"
            f"Product Category: {opp.product_sub_category or 'General'}"
        )

        timeline_block = (
            f"[TIMELINE]\n"
            f"Expected Close Date: {close_date} | Actual Close Date: {actual_close}\n"
            f"Next Follow-up: {opp.next_followup_type or 'None'} on {opp.next_followup_date or 'TBD'}\n"
            f"Pipeline Age: {opp.how_old_days or 0} Days Open | Untouched For: {opp.untouched_since_days or 0} Days"
        )
        
        if opp.sales_stage == 'Closed Lost':
            timeline_block += f"\nReason for Loss: {opp.lost_reason or 'Not Specified'}"

        automation_block = (
            f"[AUTOMATION STATUS]\n"
            f"Contract Automation: {'Yes' if opp.contract_automation else 'No'}\n"
            f"Contract Created: {'Yes' if opp.contract_created else 'No'} (Last Contract ID: {opp.last_contract_id or 'None'})\n"
            f"Current Opportunity: {'Yes' if opp.current_opportunity else 'No'}\n"
            f"Auto Product Created: {'Yes' if opp.auto_product_created else 'No'}\n"
            f"Lead TAT: Created on {opp.lead_created_date or 'N/A'} (TAT: {opp.lead_created_tat_hours or 0} Hours)"
        )

        system_block = (
            f"[SYSTEM CONTEXT]\n"
            f"Deal Owner: {owner_name}\n"
            f"Team ID: {opp.team_id or 'Global'} | Team Set ID: {opp.team_set_id or 'N/A'}\n"
            f"Description: {opp.description or 'No description.'}\n"
            f"Latest Comment: {opp.latest_comment or '-'}"
        )

        return f"{overview_block}\n\n{commercials_block}\n\n{timeline_block}\n\n{automation_block}\n\n{system_block}"

    # orchestrator
    def _get_all_data_as_text(self):
        all_text_chunks = []
        
        user_map = self._get_user_map()

        users = UserRepository.get_all_users()
        for user in users:
            all_text_chunks.append(self._format_user_to_text(user))

        accounts = AccountRepository.get_all_accounts()
        for acc in accounts:
            all_text_chunks.append(self._format_account_to_text(acc, user_map))

        leads = LeadRepository.get_all_leads()
        for lead in leads:
            all_text_chunks.append(self._format_lead_to_text(lead, user_map))

        opps = OpportunityRepository.get_all_opportunities()
        for opp in opps:
            all_text_chunks.append(self._format_opportunity_to_text(opp, user_map))

        return all_text_chunks


    def train_ai(self):
        text_chunks = self._get_all_data_as_text()

        documents = []
        for chunk in text_chunks:
            documents.append(Document(page_content=chunk))

        # vectorizing and embeddings
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
        if not self.vector_store:
            self._load_vector_store()

        # semantic search
        relevant_docs = self.vector_store.similarity_search(user_query, k=10)
        
        context_text = "\n\n".join([doc.page_content for doc in relevant_docs])

        # prompt engineering
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are an expert CRM Analyst. You have access to detailed dossiers of Users, Accounts, Leads, and Opportunities. "
                       "Use the [HEADERS] in the context to find answers. "
                       "If asked about value/money, look for the [COMMERCIALS] section. "
                       "If asked about status, look for [PIPELINE STATUS]. "
                       "Answer strictly based on the context provided below."),
            ("user", "Context:\n{context}\n\nQuestion: {question}")
        ])

        chain = prompt_template | self.llm

        response = chain.invoke({
            "context": context_text,
            "question": user_query
        })

        return [response.content]