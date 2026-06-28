from services.data_manager import DataManager

class SpeedService:
    @staticmethod
    def speed_order(team):
        data = DataManager.get_animus_data()
        
        team_data = []
        
        for animus in team:
            if animus in data:
                team_data.append({
                    "name": animus,
                    "priority": data[animus]["speed_priority"]
                })
        
        team_data.sort(
            key = lambda x: x["priority"]
        )
        
        return team_data