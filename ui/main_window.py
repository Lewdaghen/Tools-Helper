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
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        self.current_module = None
        self.skin_processor_tab = None
        
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
        main_frame = self.create_frame(self.root, AppTheme.BG_DARK)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.setup_header(main_frame)
        self.setup_content_area(main_frame)
    
    def create_frame(self, parent, bg_color, **kwargs):
        frame = tk.Frame(parent, bg=bg_color, **kwargs)
        return frame
    
    def create_label(self, parent, text, bg_color, fg_color, font, **kwargs):
        label = tk.Label(
            parent,
            text=text,
            bg=bg_color,
            fg=fg_color,
            font=font,
            **kwargs
        )
        return label
    
    def create_button(self, parent, text, command, style_variant="primary", custom_font=None, **kwargs):
        button_style = AppTheme.get_button_style(style_variant).copy()
        if custom_font:
            button_style['font'] = custom_font
        button_style.update(kwargs)
        
        button = tk.Button(
            parent,
            text=text,
            command=command,
            **button_style
        )
        return button
    
    def setup_header(self, parent):
        header_frame = self.create_frame(parent, AppTheme.BG_CARD, height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        header_content = self.create_frame(header_frame, AppTheme.BG_CARD)
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        self.setup_header_title(header_content)
        self.setup_header_controls(header_content)
        
        self.update_header()
    
    def setup_header_title(self, parent):
        title_frame = self.create_frame(parent, AppTheme.BG_CARD)
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.create_label(
            title_frame,
            "🛠️ Tools Helper",
            AppTheme.BG_CARD,
            AppTheme.TEXT_ACCENT,
            ("Segoe UI", 18, "bold")
        ).pack(anchor="w")
        
        self.create_label(
            title_frame,
            "CSLoL Skin Manager",
            AppTheme.BG_CARD,
            AppTheme.TEXT_SECONDARY,
            ("Segoe UI", 11)
        ).pack(anchor="w")
    
    def setup_header_controls(self, parent):
        path_frame = self.create_frame(parent, AppTheme.BG_CARD)
        path_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.path_var = tk.StringVar()
        self.path_label = self.create_label(
            path_frame,
            "",
            AppTheme.BG_CARD,
            AppTheme.TEXT_SECONDARY,
            ("Segoe UI", 10),
            textvariable=self.path_var,
            anchor="e"
        )
        self.path_label.pack(anchor="e", pady=(0, 5))
        
        configure_btn = self.create_button(
            path_frame,
            "🔧 Configure Path",
            self.configure_path,
            custom_font=("Segoe UI", 9),
            padx=15,
            pady=5
        )
        configure_btn.pack(anchor="e")
    
    def setup_content_area(self, parent):
        content_frame = self.create_frame(parent, AppTheme.BG_DARK)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.setup_sidebar(content_frame)
        self.setup_main_content(content_frame)
        self.switch_module("skin_processor")
    
    def setup_sidebar(self, parent):
        sidebar_frame = self.create_frame(parent, AppTheme.BG_MEDIUM, width=250)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sidebar_frame.pack_propagate(False)
        
        sidebar_content = self.create_frame(sidebar_frame, AppTheme.BG_MEDIUM)
        sidebar_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=20)
        
        self.setup_modules_section(sidebar_content)
        self.setup_info_section(sidebar_content)
    
    def setup_modules_section(self, parent):
        self.create_label(
            parent,
            "📚 MODULES",
            AppTheme.BG_MEDIUM,
            AppTheme.PRIMARY,
            ("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(0, 15))
        
        self.skin_processor_btn = tk.Button(
            parent,
            text="🎨 Skin Processor",
            command=lambda: self.switch_module("skin_processor"),
            bg=AppTheme.BG_MEDIUM,
            fg=AppTheme.TEXT_ACCENT,
            activebackground=AppTheme.PRIMARY,
            activeforeground=AppTheme.TEXT_PRIMARY,
            relief="flat",
            borderwidth=0,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            anchor="w",
            padx=15,
            pady=12
        )
        self.skin_processor_btn.pack(fill=tk.X, pady=(0, 5))
    
    def setup_info_section(self, parent):
        separator = self.create_frame(parent, AppTheme.BORDER, height=1)
        separator.pack(fill=tk.X, pady=20)
        
        self.create_label(
            parent,
            "ℹ️ INFORMATION",
            AppTheme.BG_MEDIUM,
            AppTheme.PRIMARY,
            ("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(0, 10))
        
        self.create_label(
            parent,
            "Select a module from\nthe list above to\nget started.",
            AppTheme.BG_MEDIUM,
            AppTheme.TEXT_SECONDARY,
            ("Segoe UI", 10),
            justify=tk.LEFT,
            anchor="w"
        ).pack(anchor="w")
    
    def setup_main_content(self, parent):
        self.main_content_frame = self.create_frame(parent, AppTheme.BG_DARK)
        self.main_content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    def switch_module(self, module_name):
        if self.current_module == module_name:
            return
        
        if not hasattr(self, 'main_content_frame') or not self.main_content_frame:
            return
            
        self.update_sidebar_selection(module_name)
        self.clear_main_content()
        self.load_module(module_name)
        
        self.current_module = module_name
    
    def update_sidebar_selection(self, module_name):
        is_selected = module_name == "skin_processor"
        self.skin_processor_btn.configure(
            bg=AppTheme.PRIMARY if is_selected else AppTheme.BG_MEDIUM,
            fg=AppTheme.TEXT_PRIMARY if is_selected else AppTheme.TEXT_ACCENT
        )
    
    def clear_main_content(self):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()
    
    def load_module(self, module_name):
        if module_name == "skin_processor":
            self.skin_processor_tab = SkinProcessorTab(self.main_content_frame, self.config, self.logger)
    
    def update_header(self):
        path = self.config.get_cslol_path()
        if path and self.config.validate_cslol_path():
            self.path_var.set(f"✅ {path}")
            self.path_label.configure(fg=AppTheme.SUCCESS)
        elif path:
            self.path_var.set(f"❌ {path} (Invalid)")
            self.path_label.configure(fg=AppTheme.ERROR)
        else:
            self.path_var.set("⚠️ Path not configured")
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
                
                if self.skin_processor_tab and hasattr(self.skin_processor_tab, 'load_skins'):
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