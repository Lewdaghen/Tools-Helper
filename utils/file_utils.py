import shutil
import threading
import time
import random
import gc
from pathlib import Path

class FileManager:
    @staticmethod
    def force_remove_directory(directory, logger=None):
        if not directory.exists():
            return True
        
        try:
            shutil.rmtree(directory)
            return True
        except (PermissionError, OSError) as e:
            if logger:
                logger.log(f"Warning: Cannot remove {directory.name} - {e}")
        
        for attempt in range(3):
            if logger:
                logger.log(f"Attempt {attempt + 1}/3...")
            gc.collect()
            time.sleep(2)
            try:
                shutil.rmtree(directory)
                if logger:
                    logger.log(f"✓ Removal successful at attempt {attempt + 1}")
                return True
            except (PermissionError, OSError):
                continue
        
        try:
            backup_name = f"{directory.name}_old_{random.randint(1000, 9999)}"
            backup_dir = directory.parent / backup_name
            
            if logger:
                logger.log(f"Renaming {directory.name} to {backup_name}")
            directory.rename(backup_dir)
            
            threading.Thread(target=FileManager.cleanup_old_directory, args=(backup_dir, logger), daemon=True).start()
            return True
            
        except Exception as e:
            if logger:
                logger.log(f"Cannot rename: {e}")
        
        raise Exception(f"Cannot clean directory {directory.name}.\n\n"
                       "Possible solutions:\n"
                       "• Close all file explorers\n"
                       "• Restart the application\n"
                       "• Manually delete the 'process' folder")
    
    @staticmethod
    def cleanup_old_directory(directory, logger=None):
        for i in range(10):
            time.sleep(60)
            try:
                if directory.exists():
                    shutil.rmtree(directory)
                    if logger:
                        logger.log(f"✓ Old directory {directory.name} cleaned automatically")
                break
            except:
                continue
    
    @staticmethod
    def generate_unique_dir_name(base_name):
        timestamp = int(time.time()) % 10000
        random_id = random.randint(100, 999)
        return f"{base_name}_{timestamp}_{random_id}"
    
    @staticmethod
    def cleanup_old_work_directories(base_path, patterns, logger=None):
        for pattern in patterns:
            old_dirs = list(base_path.glob(pattern))
            for old_dir in old_dirs:
                try:
                    shutil.rmtree(old_dir)
                    if logger:
                        logger.log(f"Cleaned old directory: {old_dir.name}")
                except:
                    if logger:
                        logger.log(f"Could not clean: {old_dir.name}") 