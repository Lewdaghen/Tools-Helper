class AppTheme:
    PRIMARY = "#8B5CF6"
    PRIMARY_LIGHT = "#A78BFA"
    PRIMARY_DARK = "#7C3AED"
    
    SECONDARY = "#6366F1"
    SECONDARY_LIGHT = "#818CF8"
    SECONDARY_DARK = "#4F46E5"
    
    BG_DARK = "#1E1B2E"
    BG_MEDIUM = "#2A2438"
    BG_LIGHT = "#393050"
    BG_CARD = "#312B47"
    
    TEXT_PRIMARY = "#F8FAFC"
    TEXT_SECONDARY = "#CBD5E1"
    TEXT_MUTED = "#94A3B8"
    TEXT_ACCENT = "#C084FC"
    
    SUCCESS = "#10B981"
    WARNING = "#F59E0B"
    ERROR = "#EF4444"
    INFO = "#3B82F6"
    
    HOVER = "#4C1D95"
    ACTIVE = "#5B21B6"
    DISABLED = "#4B5563"
    
    BORDER = "#475569"
    BORDER_LIGHT = "#64748B"
    BORDER_ACCENT = "#8B5CF6"
    
    @classmethod
    def configure_style(cls, root):
        root.configure(bg=cls.BG_DARK)
        style_config = {
            'TFrame': {
                'configure': {'background': cls.BG_DARK}
            },
            'TLabel': {
                'configure': {
                    'background': cls.BG_DARK,
                    'foreground': cls.TEXT_PRIMARY,
                    'font': ('Segoe UI', 10)
                }
            },
            'TButton': {
                'configure': {
                    'background': cls.PRIMARY,
                    'foreground': cls.TEXT_PRIMARY,
                    'borderwidth': 0,
                    'focuscolor': 'none',
                    'font': ('Segoe UI', 10),
                    'padding': (16, 8)
                },
                'map': {
                    'background': [
                        ('active', cls.PRIMARY_LIGHT),
                        ('pressed', cls.PRIMARY_DARK)
                    ]
                }
            },
            'TNotebook': {
                'configure': {
                    'background': cls.BG_DARK,
                    'borderwidth': 0,
                    'tabmargins': [2, 5, 2, 0]
                }
            },
            'TNotebook.Tab': {
                'configure': {
                    'background': cls.BG_MEDIUM,
                    'foreground': cls.TEXT_SECONDARY,
                    'padding': [20, 12],
                    'font': ('Segoe UI', 10)
                },
                'map': {
                    'background': [
                        ('selected', cls.PRIMARY),
                        ('active', cls.BG_LIGHT)
                    ],
                    'foreground': [
                        ('selected', cls.TEXT_PRIMARY),
                        ('active', cls.TEXT_PRIMARY)
                    ]
                }
            },
            'TProgressbar': {
                'configure': {
                    'background': cls.PRIMARY,
                    'troughcolor': cls.BG_MEDIUM,
                    'borderwidth': 0,
                    'lightcolor': cls.PRIMARY_LIGHT,
                    'darkcolor': cls.PRIMARY_DARK
                }
            }
        }
        
        return style_config
    
    @classmethod
    def get_button_style(cls, variant="primary"):
        styles = {
            'primary': {
                'bg': cls.PRIMARY,
                'fg': cls.TEXT_PRIMARY,
                'activebackground': cls.PRIMARY_LIGHT,
                'activeforeground': cls.TEXT_PRIMARY,
                'relief': 'flat',
                'borderwidth': 0,
                'font': ('Segoe UI', 10),
                'cursor': 'hand2'
            },
            'secondary': {
                'bg': cls.BG_LIGHT,
                'fg': cls.TEXT_PRIMARY,
                'activebackground': cls.HOVER,
                'activeforeground': cls.TEXT_PRIMARY,
                'relief': 'flat',
                'borderwidth': 0,
                'font': ('Segoe UI', 10),
                'cursor': 'hand2'
            },
            'success': {
                'bg': cls.SUCCESS,
                'fg': cls.TEXT_PRIMARY,
                'activebackground': '#059669',
                'activeforeground': cls.TEXT_PRIMARY,
                'relief': 'flat',
                'borderwidth': 0,
                'font': ('Segoe UI', 10),
                'cursor': 'hand2'
            }
        }
        return styles.get(variant, styles['primary'])
    
    @classmethod
    def get_listbox_style(cls):
        return {
            'bg': cls.BG_CARD,
            'fg': cls.TEXT_PRIMARY,
            'selectbackground': cls.PRIMARY,
            'selectforeground': cls.TEXT_PRIMARY,
            'highlightthickness': 1,
            'highlightcolor': cls.BORDER_ACCENT,
            'highlightbackground': cls.BORDER,
            'borderwidth': 0,
            'font': ('Segoe UI', 10),
            'activestyle': 'none'
        }
    
    @classmethod
    def get_text_style(cls):
        return {
            'bg': cls.BG_CARD,
            'fg': cls.TEXT_PRIMARY,
            'insertbackground': cls.TEXT_PRIMARY,
            'selectbackground': cls.PRIMARY,
            'selectforeground': cls.TEXT_PRIMARY,
            'highlightthickness': 1,
            'highlightcolor': cls.BORDER_ACCENT,
            'highlightbackground': cls.BORDER,
            'borderwidth': 0,
            'font': ('Consolas', 9),
            'wrap': 'word'
        } 