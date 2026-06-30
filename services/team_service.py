from services.data_manager import DataManager

class TeamService:
    @staticmethod
    def get_animus_teams(animus):
        key = animus.strip().lower()
        
        unit = DataManager.get_animus_entry(key)
        
        if not unit:
            return None
        
        return {
            "name": unit.get('name'),
            "image": unit.get('image'),
            "element": unit.get('element'),
            "teams": unit.get('teams')
        }