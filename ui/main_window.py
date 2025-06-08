import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from .skin_processor_tab import SkinProcessorTab

class MainWindow:
    def __init__(self, config_manager, logger):
        self.config = config_manager
        self.logger = logger
        
        self.root = tk.Tk()
        self.root.title("Tools Helper")
        self.root.geometry("900x700")
        
        self.setup_ui()
        self.check_initial_config()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        self.setup_header(main_frame)
        self.setup_notebook(main_frame)
    
    def setup_header(self, parent):
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        ttk.Label(header_frame, text="CSLoL Manager Path:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.path_var = tk.StringVar()
        self.path_label = ttk.Label(header_frame, textvariable=self.path_var, foreground="gray")
        self.path_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(header_frame, text="Configure", command=self.configure_path).grid(row=0, column=2)
        
        self.update_header()
    
    def setup_notebook(self, parent):
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.skin_processor_tab = SkinProcessorTab(self.notebook, self.config, self.logger)
        self.notebook.add(self.skin_processor_tab.frame, text="Skin Processor")
        
    def update_header(self):
        path = self.config.get_cslol_path()
        if path and self.config.validate_cslol_path():
            self.path_var.set(f"✓ {path}")
            self.path_label.configure(foreground="green")
        elif path:
            self.path_var.set(f"✗ {path} (Invalid)")
            self.path_label.configure(foreground="red")
        else:
            self.path_var.set("Not configured")
            self.path_label.configure(foreground="gray")
    
    def configure_path(self):
        initial_dir = self.config.get_cslol_path() or str(Path.home())
        
        path = filedialog.askdirectory(
            title="Select CSLoL Manager Directory",
            initialdir=initial_dir
        )
        
        if path:
            path_obj = Path(path)
            if (path_obj / "installed").exists():
                self.config.set_cslol_path(path)
                self.update_header()
                self.logger.log(f"CSLoL Manager path set to: {path}")
                
                if hasattr(self.skin_processor_tab, 'load_skins'):
                    self.skin_processor_tab.load_skins()
            else:
                messagebox.showerror("Error", "Invalid CSLoL Manager directory.\nMust contain 'installed' folder.")
    
    def check_initial_config(self):
        if not self.config.validate_cslol_path():
            result = messagebox.askyesno(
                "Configuration Required", 
                "CSLoL Manager path is not configured.\nWould you like to configure it now?"
            )
            if result:
                self.configure_path()
    
    def run(self):
        self.root.mainloop() 