import json
from pathlib import Path


class DataManager:
    _json_cache = {}
    _animus_lookup = None

    @classmethod
    def load_json(cls, filename):
        if filename not in cls._json_cache:
            data_path = Path(__file__).resolve().parent.parent / 'data' / filename
            
            with data_path.open('r', encoding='utf-8') as file:
                cls._json_cache[filename] = json.load(file)
                
        return cls._json_cache[filename]

    @classmethod
    def get_animus_data(cls):
        return cls.load_json('animus.json')

    @classmethod
    def get_animus_entry(cls, animus):
        if not isinstance(animus, str):
            return None

        data = cls.get_animus_data()
        
        if not data:
            return None

        if cls._animus_lookup is None:
            cls._animus_lookup = {str(key).strip().lower(): key for key in data}

        key = cls._animus_lookup.get(animus.strip().lower())
        
        return data.get(key) if key is not None else None