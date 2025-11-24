from repositories.OpportunityRepository import OpportunityRepository

class OpportunityService:
    @staticmethod
    def create_opportunity(data):
        return OpportunityRepository.add_opportunity(data)

    @staticmethod
    def get_all_opportunities():
        return OpportunityRepository.get_all_opportunities()

    @staticmethod
    def get_opportunity_by_id(opp_id):
        return OpportunityRepository.get_opportunity_by_id(opp_id)

    @staticmethod
    def update_opportunity(opp_id, data):
        return OpportunityRepository.update_opportunity(opp_id, data)

    @staticmethod
    def delete_opportunity(opp_id):
        return OpportunityRepository.delete_opportunity(opp_id)