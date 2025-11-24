from repositories.LeadRepository import LeadRepository

class LeadService:
    @staticmethod
    def create_lead(data):
        return LeadRepository.add_lead(data)

    @staticmethod
    def get_all_leads():
        return LeadRepository.get_all_leads()

    @staticmethod
    def get_lead_by_id(lead_id):
        return LeadRepository.get_lead_by_id(lead_id)

    @staticmethod
    def update_lead(lead_id, data):
        return LeadRepository.update_lead(lead_id, data)

    @staticmethod
    def delete_lead(lead_id):
        return LeadRepository.delete_lead(lead_id)