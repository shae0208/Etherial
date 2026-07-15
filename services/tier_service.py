from services.data_manager import DataManager

class TierService:
    @staticmethod
    def get_tierlist():
        data = DataManager.get_animus_data() or {}
        
        grouped = {'T0': [], 'T0.5': [], 'T1': [], 'T2': [], 'T3': [], 'T4': [], 'T5': []}

        for unit in data.values():
            if not isinstance(unit, dict):
                continue

            tier = str(unit.get('tier', '')).strip().upper()
            name = unit.get('name')

            if tier in grouped and name:
                grouped[tier].append(name)

        for names in grouped.values():
            names.sort(key=str.lower)

        return grouped