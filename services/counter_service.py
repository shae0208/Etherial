from services.data_manager import DataManager


class CounterService:
    @staticmethod
    def get_counters(animus):
        key = animus.strip().lower()
        
        unit = DataManager.get_animus_entry(key)

        if not unit:
            return None

        return {
            "name": unit.get('name'),
            "image": unit.get('image'),
            "element": unit.get('element'),
            "counters": unit.get('counters'),
            "countered_by": unit.get('countered_by')
        }