from services.data_manager import DataManager


class AnimusService:
    @staticmethod
    def get_supported_animus():
        data = DataManager.get_animus_data() or {}
        grouped = {'SSR': [], 'SR': [], 'R': []}

        for unit in data.values():
            if not isinstance(unit, dict):
                continue

            rarity = str(unit.get('rarity', '')).strip().upper()
            name = unit.get('name')

            if rarity in grouped and name:
                grouped[rarity].append(name)

        for names in grouped.values():
            names.sort(key=str.lower)

        return grouped