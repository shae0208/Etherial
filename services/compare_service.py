from services.data_manager import DataManager

class CompareService:
    @staticmethod
    def get_comparison_data(animus1, animus2):
        key1 = animus1.strip().lower()
        key2 = animus2.strip().lower()
        
        unit1 = DataManager.get_animus_entry(key1)
        unit2 = DataManager.get_animus_entry(key2)
        
        if not unit1 or not unit2:
            return None
        
        return {
            "animus1": unit1,
            "animus2": unit2
        }