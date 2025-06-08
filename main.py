#!/usr/bin/env python3

from config.config_manager import ConfigManager
from utils.logging_utils import LogHandler
from ui.main_window import MainWindow

def main():
    config_manager = ConfigManager()
    logger = LogHandler()
    
    app = MainWindow(config_manager, logger)
    app.run()

if __name__ == "__main__":
    main() 