import customtkinter as ctk
import os
from Basic import ImageEditor as BasicEditor
from Filters import ImageEditorApp
from Seg import ModernImageSegmentation  # Import the class from Seg.py
from Style import StyleTransferApp  # Import the StyleTransferApp class

class EasyEditsApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("EasyEdits")
        self.geometry("800x600")
        self.configure(fg_color="#1a1a1a")  # Dark background

        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Configure buttons with consistent styling
        button_color = "#ffff80"  # Light yellow
        text_color = "#000000"    # Black text
        button_font = ("Poppins", 24)
        corner_radius = 15

        # Create left frame
        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        left_frame.grid_rowconfigure((0, 1), weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        # Create Basics button
        basics_button = ctk.CTkButton(
            left_frame,
            text="Basics",
            font=button_font,
            fg_color=button_color,
            text_color=text_color,
            hover_color="#e6e673",
            corner_radius=corner_radius,
            height=80,
            command=self.open_basics
        )
        basics_button.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        # Create Advanced button
        advanced_button = ctk.CTkButton(
            left_frame,
            text="Advanced",
            font=button_font,
            fg_color=button_color,
            text_color=text_color,
            hover_color="#e6e673",
            corner_radius=corner_radius,
            height=80,
            command=self.open_advanced
        )
        advanced_button.grid(row=1, column=0, sticky="nsew")

        # Create right frame
        right_frame = ctk.CTkFrame(self, fg_color="transparent")
        right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        right_frame.grid_rowconfigure((0, 1), weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        # Create Image Segmentation button
        segment_button = ctk.CTkButton(
            right_frame,
            text="Image\nSegmentation",
            font=button_font,
            fg_color=button_color,
            text_color=text_color,
            hover_color="#e6e673",
            corner_radius=corner_radius,
            height=80,
            command=self.open_segmentation
        )
        segment_button.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        # Create Style Transfer button
        style_button = ctk.CTkButton(
            right_frame,
            text="Style\nTransfer",
            font=button_font,
            fg_color=button_color,
            text_color=text_color,
            hover_color="#e6e673",
            corner_radius=corner_radius,
            height=80,
            command=self.open_style_transfer  # Add command to open Style Transfer
        )
        style_button.grid(row=1, column=0, sticky="nsew")

    def open_basics(self):
        self.destroy()
        editor = BasicEditor()
        editor.run()

    def open_advanced(self):
        self.destroy()
        editor = ImageEditorApp()
        editor.mainloop()

    def open_segmentation(self):
        self.destroy()
        segmentation = ModernImageSegmentation()  # Instantiate the ModernImageSegmentation class
        segmentation.run()

    def open_style_transfer(self):
        self.withdraw()  # Hide the current window instead of destroying it
        style_transfer_app = StyleTransferApp(original_window=self)  # Pass the current window as reference
        style_transfer_app.run()

class GetStart(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Get Started")

        # Set up the main window frame
        self.pack(pady=20, padx=20, fill="both", expand=True)

        # Get Started button
        self.get_started_btn = ctk.CTkButton(
            self,
            text="Get Started!",
            width=200,
            height=50,
            fg_color="#80c1ff",
            text_color="white",
            hover_color="#4da6ff",
            corner_radius=10,
            command=self.open_advanced
        )
        self.get_started_btn.pack(pady=20)

    def open_advanced(self):
        self.pack_forget()
        app = ImageEditorApp()
        app.mainloop()

if __name__ == "__main__":
    app = EasyEditsApp()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app.mainloop()
