from services.data_manager import DataManager

class TeamService:
    @staticmethod
    def get_teams(animus):
        unit = DataManager.get_animus_entry(animus)
        
        if not unit:
            return None
        
        return {
            "name": unit.get('name'),
            "image": unit.get('image'),
            "teams": unit.get('teams')
        }