import tkinter as tk
from tkinter import ttk, messagebox
import threading
from features.skin_processor.processor import SkinProcessor
from .theme import AppTheme

class SkinProcessorTab:
    def __init__(self, parent, config_manager, logger):
        self.parent = parent
        self.config = config_manager
        self.logger = logger
        self.processor = None
        
        self.setup_ui()
        self.load_skins()
    
    def setup_ui(self):
        self.frame = tk.Frame(self.parent, bg=AppTheme.BG_DARK)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.setup_selection_section()
        self.setup_skin_list()
        self.setup_buttons()
        self.setup_progress_section()
        self.setup_logs_section()
    
    def setup_selection_section(self):
        selection_card = tk.Frame(self.frame, bg=AppTheme.BG_CARD, relief="flat", bd=0)
        selection_card.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        title_frame = tk.Frame(selection_card, bg=AppTheme.BG_CARD)
        title_frame.pack(fill=tk.X, padx=20, pady=15)
        
        title_label = tk.Label(
            title_frame,
            text="🎯 Skin Selection",
            bg=AppTheme.BG_CARD,
            fg=AppTheme.TEXT_PRIMARY,
            font=("Segoe UI", 14, "bold")
        )
        title_label.pack(anchor="w")
        
        subtitle_label = tk.Label(
            title_frame,
            text="Choose the skins to process from the list below",
            bg=AppTheme.BG_CARD,
            fg=AppTheme.TEXT_SECONDARY,
            font=("Segoe UI", 10)
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
    
    def setup_skin_list(self):
        list_card = tk.Frame(self.frame, bg=AppTheme.BG_CARD, relief="flat", bd=0)
        list_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        list_header = tk.Frame(list_card, bg=AppTheme.BG_CARD)
        list_header.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        list_title = tk.Label(
            list_header,
            text="📋 Available Skins",
            bg=AppTheme.BG_CARD,
            fg=AppTheme.TEXT_PRIMARY,
            font=("Segoe UI", 12, "bold")
        )
        list_title.pack(anchor="w")
        
        listbox_frame = tk.Frame(list_card, bg=AppTheme.BG_CARD)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        self.skin_listbox = tk.Listbox(
            listbox_frame, 
            selectmode=tk.MULTIPLE, 
            height=12,
            **AppTheme.get_listbox_style()
        )
        self.skin_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(
            listbox_frame, 
            orient=tk.VERTICAL, 
            command=self.skin_listbox.yview,
            bg=AppTheme.BG_MEDIUM,
            troughcolor=AppTheme.BG_CARD,
            activebackground=AppTheme.PRIMARY,
            highlightthickness=0,
            bd=0
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        self.skin_listbox.configure(yscrollcommand=scrollbar.set)
    
    def setup_buttons(self):
        button_card = tk.Frame(self.frame, bg=AppTheme.BG_CARD, relief="flat", bd=0)
        button_card.pack(fill=tk.X, padx=10, pady=5)
        
        button_frame = tk.Frame(button_card, bg=AppTheme.BG_CARD)
        button_frame.pack(padx=20, pady=15)
        
        select_all_btn = tk.Button(
            button_frame,
            text="✅ Select All",
            command=self.select_all,
            **AppTheme.get_button_style("secondary"),
            padx=15,
            pady=8
        )
        select_all_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        deselect_all_btn = tk.Button(
            button_frame,
            text="❌ Deselect All",
            command=self.deselect_all,
            **AppTheme.get_button_style("secondary"),
            padx=15,
            pady=8
        )
        deselect_all_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        process_btn = tk.Button(
            button_frame,
            text="🚀 Process Skins",
            command=self.start_processing,
            **AppTheme.get_button_style("success"),
            padx=20,
            pady=10
        )
        process_btn.pack(side=tk.LEFT)
    
    def setup_progress_section(self):
        progress_card = tk.Frame(self.frame, bg=AppTheme.BG_CARD, relief="flat", bd=0)
        progress_card.pack(fill=tk.X, padx=10, pady=5)
        
        progress_inner = tk.Frame(progress_card, bg=AppTheme.BG_CARD)
        progress_inner.pack(fill=tk.X, padx=20, pady=15)
        
        status_frame = tk.Frame(progress_inner, bg=AppTheme.BG_CARD)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        status_icon = tk.Label(
            status_frame,
            text="⚡",
            bg=AppTheme.BG_CARD,
            fg=AppTheme.PRIMARY,
            font=("Segoe UI", 16)
        )
        status_icon.pack(side=tk.LEFT, padx=(0, 15))
        
        self.progress_var = tk.StringVar(value="Ready to process")
        self.progress_label = tk.Label(
            status_frame,
            textvariable=self.progress_var,
            bg=AppTheme.BG_CARD,
            fg=AppTheme.TEXT_PRIMARY,
            font=("Segoe UI", 11, "bold"),
            anchor="w"
        )
        self.progress_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.progress_bar = ttk.Progressbar(
            progress_inner, 
            mode='indeterminate',
            style='TProgressbar'
        )
        self.progress_bar.pack(fill=tk.X)
    
    def setup_logs_section(self):
        logs_card = tk.Frame(self.frame, bg=AppTheme.BG_CARD, relief="flat", bd=0)
        logs_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))
        
        logs_header = tk.Frame(logs_card, bg=AppTheme.BG_CARD)
        logs_header.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        logs_title = tk.Label(
            logs_header,
            text="📝 Activity Log",
            bg=AppTheme.BG_CARD,
            fg=AppTheme.TEXT_PRIMARY,
            font=("Segoe UI", 12, "bold")
        )
        logs_title.pack(anchor="w")
        
        logs_subtitle = tk.Label(
            logs_header,
            text="Follow the processing progress in real time",
            bg=AppTheme.BG_CARD,
            fg=AppTheme.TEXT_SECONDARY,
            font=("Segoe UI", 10)
        )
        logs_subtitle.pack(anchor="w", pady=(2, 0))
        
        log_frame = tk.Frame(logs_card, bg=AppTheme.BG_CARD)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        self.log_text = tk.Text(
            log_frame, 
            height=8, 
            state=tk.DISABLED,
            **AppTheme.get_text_style()
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        log_scrollbar = tk.Scrollbar(
            log_frame, 
            orient=tk.VERTICAL, 
            command=self.log_text.yview,
            bg=AppTheme.BG_MEDIUM,
            troughcolor=AppTheme.BG_CARD,
            activebackground=AppTheme.PRIMARY,
            highlightthickness=0,
            bd=0
        )
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.logger.set_log_widget(self.log_text)
    
    def load_skins(self):
        if not self.config.validate_cslol_path():
            self.logger.log("⚠️ CSLoL Manager path not configured!")
            return
        
        self.processor = SkinProcessor(self.config, self.logger)
        skins = self.processor.get_available_skins()
        skins.sort()
        
        self.skin_listbox.delete(0, tk.END)
        for skin in skins:
            self.skin_listbox.insert(tk.END, f"🎨 {skin}")
            
        self.logger.log(f"✅ {len(skins)} skins found in installed directory")
    
    def select_all(self):
        self.skin_listbox.select_set(0, tk.END)
        
    def deselect_all(self):
        self.skin_listbox.selection_clear(0, tk.END)
    
    def start_processing(self):
        if not self.config.validate_cslol_path():
            messagebox.showerror("Error", "CSLoL Manager path not configured!")
            return
        
        selected_indices = self.skin_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one skin to process!")
            return
        
        selected_skins = []
        for i in selected_indices:
            skin_text = self.skin_listbox.get(i)
            skin_name = skin_text.replace("🎨 ", "")
            selected_skins.append(skin_name)
        
        self.progress_var.set(f"Processing {len(selected_skins)} skins...")
        self.progress_bar.start(10)
        
        processing_thread = threading.Thread(
            target=self.process_skins_thread,
            args=(selected_skins,),
            daemon=True
        )
        processing_thread.start()
    
    def process_skins_thread(self, selected_skins):
        try:
            if not self.processor:
                self.processor = SkinProcessor(self.config, self.logger)
            
            self.processor.process_skins(selected_skins)
            
            self.frame.after(0, lambda: self.progress_var.set("✅ Processing completed successfully!"))
            self.frame.after(0, self.progress_bar.stop)
            
        except Exception as e:
            error_msg = f"❌ Processing failed: {str(e)}"
            self.frame.after(0, lambda: self.progress_var.set(error_msg))
            self.frame.after(0, self.progress_bar.stop)
            self.frame.after(0, lambda: messagebox.showerror("Processing Error", str(e))) 