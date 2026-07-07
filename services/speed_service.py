from services.data_manager import DataManager

class SpeedService:
    @staticmethod
    def speed_order(team):
        data = DataManager.get_animus_data()
        
        team_data = []
        
        for unit in team:
            key = unit.strip().lower()
            
            if key not in data:
                continue
            
            team_data.append({
                "name": data[key]['name'],
                "priority": data[key]['draft']["speed_priority"]
            })
        
        team_data.sort(key=lambda x: x["priority"], reverse=True)
        
        return team_data