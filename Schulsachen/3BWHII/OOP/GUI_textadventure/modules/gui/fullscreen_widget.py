import customtkinter as ctk
class FullScreenWidget(ctk.CTkFrame):
    def __init__(self, master, title, on_close_callback):
        super().__init__(master)
        self.configure(fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Main content area
        
        # Header frame
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        # Title
        ctk.CTkLabel(
            self.header_frame, 
            text=title,
            font=("Arial", 24, "bold")
        ).pack(side="left")
        
        # Close Button
        ctk.CTkButton(
            self.header_frame,
            text="X",
            width=40,
            height=40,
            fg_color="transparent",
            hover_color="#2A2D2E",
            command=on_close_callback
        ).pack(side="right")
        
        # Content frame
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)  # For items container