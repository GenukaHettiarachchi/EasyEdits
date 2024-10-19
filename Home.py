import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from GetStart import EasyEditsApp  # Import the interface from GetStart.py

class ModernApp:
    def __init__(self):
        # Set up the theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Create the main window
        self.root = ctk.CTk()
        self.root.geometry("800x600")
        self.root.title("EasyEdits")
        
        # Configure grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root, fg_color="black")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure((0,1,2,3,4), weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Logo
        self.logo_label = ctk.CTkLabel(
            self.main_frame,
            text="EasyEdits",
            font=ctk.CTkFont(family="Poppins", size=32, weight="bold"),
            text_color="white"
        )
        self.logo_label.grid(row=0, column=0, pady=(50,0))
        
        # Title labels with custom font
        self.title_label1 = ctk.CTkLabel(
            self.main_frame,
            text="Unlocking",
            font=ctk.CTkFont(family="Poppins", size=48, weight="normal"),
            text_color="white"
        )
        self.title_label1.grid(row=1, column=0)
        
        self.title_label2 = ctk.CTkLabel(
            self.main_frame,
            text="Human",
            font=ctk.CTkFont(family="Poppins", size=48, weight="normal"),
            text_color="white"
        )
        self.title_label2.grid(row=2, column=0)
        
        self.title_label3 = ctk.CTkLabel(
            self.main_frame,
            text="Potential",
            font=ctk.CTkFont(family="Poppins", size=48, weight="normal"),
            text_color="white"
        )
        self.title_label3.grid(row=3, column=0)
        
        # Create a frame for the "With GenerativeAI" text
        self.ai_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.ai_frame.grid(row=4, column=0)
        
        self.with_label = ctk.CTkLabel(
            self.ai_frame,
            text="With ",
            font=ctk.CTkFont(family="Poppins", size=48, weight="normal"),
            text_color="white"
        )
        self.with_label.pack(side="left")
        
        self.ai_label = ctk.CTkLabel(
            self.ai_frame,
            text="GenerativeAI",
            font=ctk.CTkFont(family="Poppins", size=48, weight="bold"),
            text_color="white"
        )
        self.ai_label.pack(side="left")
        
        # Get Started Button
        self.start_button = ctk.CTkButton(
            self.main_frame,
            text="Get Started!",
            font=ctk.CTkFont(family="Poppins", size=16),
            fg_color="yellow",
            text_color="black",
            hover_color="#c9c919",
            width=200,
            height=40,
            corner_radius=20,
            command=self.on_start
        )
        self.start_button.grid(row=5, column=0, pady=(0,50))
    
    def on_start(self):
        self.root.destroy()  # Close the current window
        app = EasyEditsApp()  # Create the new app window from GetStart.py
        app.mainloop()  # Run the new window
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernApp()
    app.run()
