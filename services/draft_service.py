from services.data_manager import DataManager

class DraftService:
    @staticmethod
    def recommend_ban(team):
        data = DataManager.get_animus_data()
        
        highest_priority = -1
        recommended_ban = None
        
        for unit in team:
            if unit not in data:
                continue
            
            score = data[unit]["draft"]["ban_priority"]
            
            if score > highest_priority:
                highest_priority = score
                recommended_ban = unit
            
        return recommended_ban