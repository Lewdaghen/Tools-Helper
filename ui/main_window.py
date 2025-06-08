import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from .skin_processor_tab import SkinProcessorTab
from .theme import AppTheme

class MainWindow:
    def __init__(self, config_manager, logger):
        self.config = config_manager
        self.logger = logger
        
        self.root = tk.Tk()
        self.root.title("Tools Helper - CSLoL Skin Processor")
        self.root.geometry("1000x750")
        self.root.minsize(900, 700)
        
        self.setup_theme()
        self.setup_ui()
        self.check_initial_config()
    
    def setup_theme(self):
        AppTheme.configure_style(self.root)
        
        self.style = ttk.Style()
        style_config = AppTheme.configure_style(self.root)
        
        for style_name, config in style_config.items():
            if 'configure' in config:
                self.style.configure(style_name, **config['configure'])
            if 'map' in config:
                self.style.map(style_name, **config['map'])
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        self.setup_title(main_frame)
        self.setup_header(main_frame)
        self.setup_notebook(main_frame)
    
    def setup_title(self, parent):
        title_frame = ttk.Frame(parent)
        title_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        title_label = ttk.Label(
            title_frame, 
            text="🛠️ Tools Helper", 
            font=("Segoe UI", 20, "bold")
        )
        title_label.configure(foreground=AppTheme.TEXT_ACCENT)
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        subtitle_label = ttk.Label(
            title_frame, 
            text="CSLoL Skin Manager",
            font=("Segoe UI", 12)
        )
        subtitle_label.configure(foreground=AppTheme.TEXT_SECONDARY)
        subtitle_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
    
    def setup_header(self, parent):
        header_card = tk.Frame(parent, bg=AppTheme.BG_CARD, relief="flat", bd=0)
        header_card.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        header_card.columnconfigure(1, weight=1)
        
        inner_frame = tk.Frame(header_card, bg=AppTheme.BG_CARD)
        inner_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=20, pady=15)
        inner_frame.columnconfigure(1, weight=1)
        
        path_label = tk.Label(
            inner_frame,
            text="📁 CSLoL Manager Path:",
            bg=AppTheme.BG_CARD,
            fg=AppTheme.TEXT_PRIMARY,
            font=("Segoe UI", 11, "bold")
        )
        path_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
        
        self.path_var = tk.StringVar()
        self.path_label = tk.Label(
            inner_frame,
            textvariable=self.path_var,
            bg=AppTheme.BG_CARD,
            fg=AppTheme.TEXT_SECONDARY,
            font=("Segoe UI", 10),
            anchor="w"
        )
        self.path_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 15))
        
        configure_btn = tk.Button(
            inner_frame,
            text="🔧 Configure",
            command=self.configure_path,
            **AppTheme.get_button_style("primary"),
            padx=20,
            pady=8
        )
        configure_btn.grid(row=0, column=2)
        
        self.update_header()
    
    def setup_notebook(self, parent):
        notebook_frame = tk.Frame(parent, bg=AppTheme.BG_DARK)
        notebook_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        notebook_frame.columnconfigure(0, weight=1)
        notebook_frame.rowconfigure(0, weight=1)
        
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.skin_processor_tab = SkinProcessorTab(self.notebook, self.config, self.logger)
        self.notebook.add(self.skin_processor_tab.frame, text="🎨 Skin Processor")
        
    def update_header(self):
        path = self.config.get_cslol_path()
        if path and self.config.validate_cslol_path():
            self.path_var.set(f"✅ {path}")
            self.path_label.configure(fg=AppTheme.SUCCESS)
        elif path:
            self.path_var.set(f"❌ {path} (Invalid)")
            self.path_label.configure(fg=AppTheme.ERROR)
        else:
            self.path_var.set("⚠️ Not configured")
            self.path_label.configure(fg=AppTheme.WARNING)
    
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
                messagebox.showerror(
                    "Error", 
                    "Invalid CSLoL Manager directory.\nMust contain 'installed' folder.",
                    icon="error"
                )
    
    def check_initial_config(self):
        if not self.config.validate_cslol_path():
            result = messagebox.askyesno(
                "Configuration Required", 
                "CSLoL Manager path is not configured.\nWould you like to configure it now?",
                icon="question"
            )
            if result:
                self.configure_path()
    
    def run(self):
        self.root.mainloop() 