import tkinter as tk
from tkinter import ttk, messagebox
import threading
from features.skin_processor.processor import SkinProcessor

class SkinProcessorTab:
    def __init__(self, parent, config_manager, logger):
        self.parent = parent
        self.config = config_manager
        self.logger = logger
        self.processor = None
        
        self.setup_ui()
        self.load_skins()
    
    def setup_ui(self):
        self.frame = ttk.Frame(self.parent, padding="10")
        
        ttk.Label(self.frame, text="Select skins to process:").grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        listbox_frame = ttk.Frame(self.frame)
        listbox_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        
        self.skin_listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, height=15)
        self.skin_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.skin_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.skin_listbox.configure(yscrollcommand=scrollbar.set)
        
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Select All", command=self.select_all).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Deselect All", command=self.deselect_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Process Skins", command=self.start_processing).pack(side=tk.LEFT, padx=(5, 0))
        
        self.progress_var = tk.StringVar(value="Ready")
        self.progress_label = ttk.Label(self.frame, textvariable=self.progress_var)
        self.progress_label.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.progress_bar = ttk.Progressbar(self.frame, mode='indeterminate')
        self.progress_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        log_frame = ttk.Frame(self.frame)
        log_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_frame, height=8, state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(5, weight=1)
        
        self.logger.set_log_widget(self.log_text)
    
    def load_skins(self):
        if not self.config.validate_cslol_path():
            self.logger.log("CSLoL Manager path not configured!")
            return
        
        self.processor = SkinProcessor(self.config, self.logger)
        skins = self.processor.get_available_skins()
        skins.sort()
        
        self.skin_listbox.delete(0, tk.END)
        for skin in skins:
            self.skin_listbox.insert(tk.END, skin)
            
        self.logger.log(f"{len(skins)} skins found in installed directory")
    
    def select_all(self):
        self.skin_listbox.select_set(0, tk.END)
        
    def deselect_all(self):
        self.skin_listbox.selection_clear(0, tk.END)
    
    def start_processing(self):
        if not self.config.validate_cslol_path():
            messagebox.showerror("Error", "Please configure CSLoL Manager first")
            return
            
        selected_indices = self.skin_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one skin!")
            return
            
        selected_skins = [self.skin_listbox.get(i) for i in selected_indices]
        
        self.progress_bar.start()
        self.progress_var.set("Processing...")
        
        threading.Thread(target=self.process_skins_thread, args=(selected_skins,), daemon=True).start()
    
    def process_skins_thread(self, selected_skins):
        try:
            if not self.processor:
                self.processor = SkinProcessor(self.config, self.logger)
            
            self.processor.process_skins(selected_skins, self.progress_var.set)
            self.progress_var.set("Completed")
            
        except Exception as e:
            self.logger.log(f"Error: {str(e)}")
            self.progress_var.set("Error")
        finally:
            self.progress_bar.stop() 