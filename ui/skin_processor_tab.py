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
        self.champion_skins = {}
        self.selected_skins = set()
        self.view_mode = "champion"
        
        self.setup_ui()
        self.load_skins()
    
    def setup_ui(self):
        self.frame = tk.Frame(self.parent, bg=AppTheme.BG_DARK)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.setup_header_section()
        self.setup_content_area()
        self.setup_bottom_section()
    
    def setup_header_section(self):
        header_card = tk.Frame(self.frame, bg=AppTheme.BG_CARD, relief="flat", bd=0)
        header_card.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        header_content = tk.Frame(header_card, bg=AppTheme.BG_CARD)
        header_content.pack(fill=tk.X, padx=20, pady=15)
        
        title_frame = tk.Frame(header_content, bg=AppTheme.BG_CARD)
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(
            title_frame,
            text="🎯 Skin Selection",
            bg=AppTheme.BG_CARD,
            fg=AppTheme.TEXT_PRIMARY,
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w")
        
        self.status_label = tk.Label(
            title_frame,
            text="Choose skins to process",
            bg=AppTheme.BG_CARD,
            fg=AppTheme.TEXT_SECONDARY,
            font=("Segoe UI", 10)
        )
        self.status_label.pack(anchor="w", pady=(5, 0))
        
        controls_frame = tk.Frame(header_content, bg=AppTheme.BG_CARD)
        controls_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Label(
            controls_frame,
            text="📊 View Mode:",
            bg=AppTheme.BG_CARD,
            fg=AppTheme.TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="e")
        
        view_controls = tk.Frame(controls_frame, bg=AppTheme.BG_CARD)
        view_controls.pack(anchor="e", pady=(5, 0))
        
        champion_style = AppTheme.get_button_style("primary").copy()
        champion_style.update({
            'font': ("Segoe UI", 9),
            'padx': 12,
            'pady': 6
        })
        self.champion_btn = tk.Button(
            view_controls,
            text="🏆 Champions",
            command=lambda: self.set_view_mode("champion"),
            **champion_style
        )
        self.champion_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        list_style = AppTheme.get_button_style("secondary").copy()
        list_style.update({
            'font': ("Segoe UI", 9),
            'padx': 12,
            'pady': 6
        })
        self.list_btn = tk.Button(
            view_controls,
            text="📋 List",
            command=lambda: self.set_view_mode("list"),
            **list_style
        )
        self.list_btn.pack(side=tk.LEFT)
    
    def setup_content_area(self):
        self.content_frame = tk.Frame(self.frame, bg=AppTheme.BG_DARK)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.setup_champion_view()
        self.setup_list_view()
        
        self.show_champion_view()
    
    def setup_champion_view(self):
        self.champion_card = tk.Frame(self.content_frame, bg=AppTheme.BG_CARD, relief="flat", bd=0)
        
        canvas_frame = tk.Frame(self.champion_card, bg=AppTheme.BG_CARD)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        self.champions_canvas = tk.Canvas(
            canvas_frame,
            bg=AppTheme.BG_CARD,
            highlightthickness=0,
            bd=0
        )
        self.champions_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        canvas_scrollbar = tk.Scrollbar(
            canvas_frame,
            orient=tk.VERTICAL,
            command=self.champions_canvas.yview,
            bg=AppTheme.BG_MEDIUM,
            troughcolor=AppTheme.BG_CARD,
            activebackground=AppTheme.PRIMARY,
            highlightthickness=0,
            bd=0
        )
        canvas_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        self.champions_canvas.configure(yscrollcommand=canvas_scrollbar.set)
        
        self.champions_grid_frame = tk.Frame(self.champions_canvas, bg=AppTheme.BG_CARD)
        self.champions_canvas_window = self.champions_canvas.create_window(
            0, 0, anchor="nw", window=self.champions_grid_frame
        )
        
        self.champions_grid_frame.bind("<Configure>", self.on_champions_frame_configure)
        self.champions_canvas.bind("<Configure>", self.on_champions_canvas_configure)
        self.champions_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
    
    def setup_list_view(self):
        self.list_card = tk.Frame(self.content_frame, bg=AppTheme.BG_CARD, relief="flat", bd=0)
        
        list_header = tk.Frame(self.list_card, bg=AppTheme.BG_CARD)
        list_header.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        tk.Label(
            list_header,
            text="📋 All Skins",
            bg=AppTheme.BG_CARD,
            fg=AppTheme.TEXT_PRIMARY,
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")
        
        listbox_frame = tk.Frame(self.list_card, bg=AppTheme.BG_CARD)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        self.skin_listbox = tk.Listbox(
            listbox_frame,
            selectmode=tk.MULTIPLE,
            height=12,
            **AppTheme.get_listbox_style()
        )
        self.skin_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        list_scrollbar = tk.Scrollbar(
            listbox_frame,
            orient=tk.VERTICAL,
            command=self.skin_listbox.yview,
            bg=AppTheme.BG_MEDIUM,
            troughcolor=AppTheme.BG_CARD,
            activebackground=AppTheme.PRIMARY,
            highlightthickness=0,
            bd=0
        )
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        self.skin_listbox.configure(yscrollcommand=list_scrollbar.set)
    
    def setup_bottom_section(self):
        self.setup_buttons()
        self.setup_progress_section()
        self.setup_logs_section()
    
    def setup_buttons(self):
        button_card = tk.Frame(self.frame, bg=AppTheme.BG_CARD, relief="flat", bd=0)
        button_card.pack(fill=tk.X, padx=10, pady=5)
        
        button_content = tk.Frame(button_card, bg=AppTheme.BG_CARD)
        button_content.pack(fill=tk.X, padx=20, pady=15)
        
        left_buttons = tk.Frame(button_content, bg=AppTheme.BG_CARD)
        left_buttons.pack(side=tk.LEFT)
        
        tk.Button(
            left_buttons,
            text="✅ Select All",
            command=self.select_all,
            **AppTheme.get_button_style("secondary"),
            padx=15,
            pady=8
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            left_buttons,
            text="❌ Clear All",
            command=self.clear_all,
            **AppTheme.get_button_style("secondary"),
            padx=15,
            pady=8
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        right_buttons = tk.Frame(button_content, bg=AppTheme.BG_CARD)
        right_buttons.pack(side=tk.RIGHT)
        
        self.selected_count_label = tk.Label(
            right_buttons,
            text="0 skins selected",
            bg=AppTheme.BG_CARD,
            fg=AppTheme.TEXT_SECONDARY,
            font=("Segoe UI", 10)
        )
        self.selected_count_label.pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Button(
            right_buttons,
            text="🚀 Process Skins",
            command=self.start_processing,
            **AppTheme.get_button_style("success"),
            padx=20,
            pady=10
        ).pack(side=tk.LEFT)
    
    def setup_progress_section(self):
        progress_card = tk.Frame(self.frame, bg=AppTheme.BG_CARD, relief="flat", bd=0)
        progress_card.pack(fill=tk.X, padx=10, pady=5)
        
        progress_inner = tk.Frame(progress_card, bg=AppTheme.BG_CARD)
        progress_inner.pack(fill=tk.X, padx=20, pady=15)
        
        status_frame = tk.Frame(progress_inner, bg=AppTheme.BG_CARD)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            status_frame,
            text="⚡",
            bg=AppTheme.BG_CARD,
            fg=AppTheme.PRIMARY,
            font=("Segoe UI", 16)
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        self.progress_var = tk.StringVar(value="Ready to process")
        tk.Label(
            status_frame,
            textvariable=self.progress_var,
            bg=AppTheme.BG_CARD,
            fg=AppTheme.TEXT_PRIMARY,
            font=("Segoe UI", 11, "bold"),
            anchor="w"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
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
        
        tk.Label(
            logs_header,
            text="📝 Activity Log",
            bg=AppTheme.BG_CARD,
            fg=AppTheme.TEXT_PRIMARY,
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")
        
        tk.Label(
            logs_header,
            text="Follow the processing progress in real time",
            bg=AppTheme.BG_CARD,
            fg=AppTheme.TEXT_SECONDARY,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(2, 0))
        
        log_frame = tk.Frame(logs_card, bg=AppTheme.BG_CARD)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        self.log_text = tk.Text(
            log_frame,
            height=6,
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
    
    def set_view_mode(self, mode):
        self.view_mode = mode
        
        if mode == "champion":
            self.champion_btn.configure(**AppTheme.get_button_style("primary"))
            self.list_btn.configure(**AppTheme.get_button_style("secondary"))
            self.show_champion_view()
        else:
            self.champion_btn.configure(**AppTheme.get_button_style("secondary"))
            self.list_btn.configure(**AppTheme.get_button_style("primary"))
            self.show_list_view()
    
    def show_champion_view(self):
        self.list_card.pack_forget()
        self.champion_card.pack(fill=tk.BOTH, expand=True)
        self.populate_champions_grid()
    
    def show_list_view(self):
        self.champion_card.pack_forget()
        self.list_card.pack(fill=tk.BOTH, expand=True)
        self.populate_skin_list()
    
    def populate_champions_grid(self):
        for widget in self.champions_grid_frame.winfo_children():
            widget.destroy()
        
        if not self.champion_skins:
            no_data_label = tk.Label(
                self.champions_grid_frame,
                text="🔍 No champions found\nConfigure CSLoL path first",
                bg=AppTheme.BG_CARD,
                fg=AppTheme.TEXT_SECONDARY,
                font=("Segoe UI", 12),
                justify=tk.CENTER
            )
            no_data_label.pack(expand=True, pady=50)
            return
        
        champions = sorted(self.champion_skins.keys())
        columns = 4
        
        for i, champion_name in enumerate(champions):
            row = i // columns
            col = i % columns
            
            champion_data = self.champion_skins[champion_name]
            emoji = champion_data['emoji']
            skins = champion_data['skins']
            
            champion_frame = tk.Frame(
                self.champions_grid_frame,
                bg=AppTheme.BG_LIGHT,
                relief="flat",
                bd=1,
                highlightbackground=AppTheme.BORDER,
                highlightcolor=AppTheme.BORDER_ACCENT,
                highlightthickness=1
            )
            champion_frame.grid(row=row, column=col, padx=8, pady=8, sticky="ew")
            
            champion_header = tk.Frame(champion_frame, bg=AppTheme.BG_LIGHT)
            champion_header.pack(fill=tk.X, padx=10, pady=(10, 5))
            
            tk.Label(
                champion_header,
                text=f"{emoji} {champion_name}",
                bg=AppTheme.BG_LIGHT,
                fg=AppTheme.TEXT_ACCENT,
                font=("Segoe UI", 11, "bold")
            ).pack()
            
            tk.Label(
                champion_header,
                text=f"{len(skins)} skin{'s' if len(skins) != 1 else ''}",
                bg=AppTheme.BG_LIGHT,
                fg=AppTheme.TEXT_SECONDARY,
                font=("Segoe UI", 9)
            ).pack()
            
            skins_frame = tk.Frame(champion_frame, bg=AppTheme.BG_LIGHT)
            skins_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
            
            for skin in skins:
                is_selected = skin in self.selected_skins
                
                skin_button = tk.Checkbutton(
                    skins_frame,
                    text=f"🎨 {skin}",
                    bg=AppTheme.BG_LIGHT,
                    fg=AppTheme.TEXT_PRIMARY if is_selected else AppTheme.TEXT_SECONDARY,
                    selectcolor=AppTheme.BG_MEDIUM,
                    activebackground=AppTheme.BG_MEDIUM,
                    activeforeground=AppTheme.TEXT_PRIMARY,
                    font=("Segoe UI", 9),
                    anchor="w",
                    relief="flat",
                    bd=0,
                    command=lambda s=skin: self.toggle_skin_selection(s)
                )
                
                if is_selected:
                    skin_button.select()
                
                skin_button.pack(fill=tk.X, pady=1)
        
        for col in range(columns):
            self.champions_grid_frame.columnconfigure(col, weight=1)
        
        self.champions_grid_frame.update_idletasks()
        self.champions_canvas.configure(scrollregion=self.champions_canvas.bbox("all"))
    
    def populate_skin_list(self):
        self.skin_listbox.delete(0, tk.END)
        
        all_skins = []
        for champion_data in self.champion_skins.values():
            all_skins.extend(champion_data['skins'])
        
        all_skins.sort()
        
        for skin in all_skins:
            self.skin_listbox.insert(tk.END, f"🎨 {skin}")
            if skin in self.selected_skins:
                self.skin_listbox.selection_set(tk.END)
    
    def toggle_skin_selection(self, skin_name):
        if skin_name in self.selected_skins:
            self.selected_skins.remove(skin_name)
        else:
            self.selected_skins.add(skin_name)
        
        self.update_selection_status()
        
        if self.view_mode == "champion":
            self.populate_champions_grid()
    
    def update_selection_status(self):
        count = len(self.selected_skins)
        self.selected_count_label.configure(
            text=f"{count} skin{'s' if count != 1 else ''} selected"
        )
        
        total_skins = sum(len(data['skins']) for data in self.champion_skins.values())
        self.status_label.configure(
            text=f"{count} of {total_skins} skins selected for processing"
        )
    
    def on_champions_frame_configure(self, event):
        self.champions_canvas.configure(scrollregion=self.champions_canvas.bbox("all"))
    
    def on_champions_canvas_configure(self, event):
        canvas_width = event.width
        self.champions_canvas.itemconfig(self.champions_canvas_window, width=canvas_width)
    
    def on_mousewheel(self, event):
        if self.view_mode == "champion" and self.champions_canvas.winfo_viewable():
            self.champions_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def load_skins(self):
        if not self.config.validate_cslol_path():
            self.logger.log("⚠️ CSLoL Manager path not configured!")
            return
        
        self.processor = SkinProcessor(self.config, self.logger)
        self.champion_skins = self.processor.get_skins_by_champion()
        
        total_skins = sum(len(data['skins']) for data in self.champion_skins.values())
        champion_count = len(self.champion_skins)
        
        self.logger.log(f"✅ Found {total_skins} skins from {champion_count} champions")
        
        if self.view_mode == "champion":
            self.populate_champions_grid()
        else:
            self.populate_skin_list()
        
        self.update_selection_status()
    
    def select_all(self):
        for champion_data in self.champion_skins.values():
            for skin in champion_data['skins']:
                self.selected_skins.add(skin)
        
        self.update_selection_status()
        
        if self.view_mode == "champion":
            self.populate_champions_grid()
        else:
            self.skin_listbox.select_set(0, tk.END)
    
    def clear_all(self):
        self.selected_skins.clear()
        self.update_selection_status()
        
        if self.view_mode == "champion":
            self.populate_champions_grid()
        else:
            self.skin_listbox.selection_clear(0, tk.END)
    
    def start_processing(self):
        if not self.config.validate_cslol_path():
            messagebox.showerror("Error", "CSLoL Manager path not configured!")
            return
        
        if not self.selected_skins:
            messagebox.showwarning("Warning", "Please select at least one skin to process!")
            return
        
        selected_list = list(self.selected_skins)
        self.progress_var.set(f"Processing {len(selected_list)} skins...")
        self.progress_bar.start(10)
        
        processing_thread = threading.Thread(
            target=self.process_skins_thread,
            args=(selected_list,),
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