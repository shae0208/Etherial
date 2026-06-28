from services.data_manager import DataManager

class CompareService:
    @staticmethod
    def compare(animus1, animus2):
        unit1 = DataManager.get_animus_entry(animus1)
        unit2 = DataManager.get_animus_entry(animus2)
        
        if not unit1 or not unit2:
            return None
        
        return {
            "animus1": unit1,
            "animus2": unit2
        }