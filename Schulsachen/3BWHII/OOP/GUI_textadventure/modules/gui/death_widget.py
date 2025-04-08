import customtkinter as ctk
from .fullscreen_widget import FullScreenWidget
from PIL import Image
from customtkinter import CTkImage
from modules.game_logic.constants import get_resource_path
import threading, time, os

class DeathWidget(FullScreenWidget):
    def __init__(self, master, on_exit_callback):
        super().__init__(master, "Game Over", on_exit_callback)
        self.on_exit_callback = on_exit_callback

        # Configure the layout
        self.grid_rowconfigure(0, weight=1)  # Center the content
        self.grid_columnconfigure(0, weight=1)

        # Create the skull animation
        self.animation_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.animation_frame.grid(row=0, column=0, sticky="nsew")

        self.skull_label = ctk.CTkLabel(self.animation_frame, text="")
        self.skull_label.pack(expand=True)

        # Load and scale the skull image to the absolute maximum
        skull_path = get_resource_path("modules/extras/skull.jpg")
        if os.path.exists(skull_path):
            skull_image = Image.open(skull_path)

            # Get the screen dimensions
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

            # Resize the image to fit the entire screen
            skull_image = skull_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)

            # Use CTkImage for HighDPI scaling
            self.skull_image = CTkImage(light_image=skull_image, size=(screen_width, screen_height))
            self.skull_label.configure(image=self.skull_image)
        else:
            self.skull_label.configure(text="💀 Game Over 💀", font=("Arial", 48, "bold"))

        # Create the "Exit" button
        self.exit_button = ctk.CTkButton(
            self,
            text="Exit Game",
            command=self.on_exit_callback,
            font=("Arial", 16, "bold"),
            fg_color="red",
            hover_color="darkred"
        )
        self.exit_button.grid(row=1, column=0, pady=20)

    def animate_skull(self):
        """Animate the skull image with a fade-in effect."""
        def fade_in():
            for alpha in range(0, 11):  # Gradually increase opacity
                self.skull_label.configure(image=self.skull_image)
                time.sleep(0.1)

        threading.Thread(target=fade_in, daemon=True).start()