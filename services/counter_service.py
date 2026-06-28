from services.data_manager import DataManager


class CounterService:
    @staticmethod
    def get_counters(animus):
        unit = DataManager.get_animus_entry(animus)

        if not unit:
            return None

        return {
            "name": unit.get('name'),
            "image": unit.get('image'),
            "counters": unit.get('counters')
        }