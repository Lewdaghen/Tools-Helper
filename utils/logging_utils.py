import tkinter as tk

class LogHandler:
    def __init__(self):
        self.log_widget = None
        self.pending_logs = []
    
    def set_log_widget(self, widget):
        self.log_widget = widget
        self.flush_pending_logs()
    
    def log(self, message):
        if self.log_widget is None:
            self.pending_logs.append(message)
            return
        
        self.log_widget.config(state=tk.NORMAL)
        self.log_widget.insert(tk.END, f"{message}\n")
        self.log_widget.see(tk.END)
        self.log_widget.config(state=tk.DISABLED)
        
        if hasattr(self.log_widget, 'master'):
            self.log_widget.master.update()
    
    def flush_pending_logs(self):
        if self.log_widget and self.pending_logs:
            for message in self.pending_logs:
                self.log(message)
            self.pending_logs.clear() 