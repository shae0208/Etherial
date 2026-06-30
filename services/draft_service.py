from services.data_manager import DataManager

class DraftService:
    @staticmethod
    def recommend_ban(team):
        data = DataManager.get_animus_data()
        
        highest_priority = -1
        recommended_ban = None
        
        for unit in team:
            key = unit.strip().lower()
            
            if key not in data:
                continue
            
            score = data[key].get('draft').get('ban_priority')
            
            if score > highest_priority:
                highest_priority = score
                recommended_ban = data[key]['name']
            
        return recommended_ban
    
    @staticmethod
    def format_team(team):
        data = DataManager.get_animus_data()
        
        formatted_team = []
        
        for unit in team:
            key = unit.strip().lower()
            
            if key in data:
                formatted_team.append(data[key]['name'])
            
        return formatted_team
            
            
        
        