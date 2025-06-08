import json
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_file = Path("config.json")
        self.config = self.load_config()
    
    def load_config(self):
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
    
    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception:
            pass
    
    def get_cslol_path(self):
        return self.config.get('cslol_manager_path', '')
    
    def set_cslol_path(self, path):
        self.config['cslol_manager_path'] = str(path)
        self.save_config()
    
    def validate_cslol_path(self):
        path = Path(self.get_cslol_path())
        if not path.exists():
            return False
        
        required_dirs = ["installed"]
        for dir_name in required_dirs:
            if not (path / dir_name).exists():
                return False
        return True 