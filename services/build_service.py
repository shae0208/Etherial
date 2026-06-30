from services.data_manager import DataManager

class BuildService:
    @staticmethod
    def get_build(animus):
        key = animus.strip().lower()
        
        unit = DataManager.get_animus_entry(key)

        if not unit:
            return None

        return {
            "name": unit.get('name'),
            "image": unit.get('image'),
            "element": unit.get('element'),
            "lattice": unit.get('lattice'),
            "build": unit.get('build')
        }