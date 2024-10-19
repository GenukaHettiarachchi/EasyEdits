import customtkinter as ctk
from PIL import Image, ImageTk, ImageFilter
import os
from tkinter import filedialog

class ImageEditorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("EasyEdits")
        self.geometry("1200x800")
        self.configure(fg_color="#1a1a1a")

        self.current_image = None  # Store current image for editing
        self.original_image = None  # Store original image for reset purposes
        self.history = []  # Store history for undo
        self.redo_history = []  # Store redo actions
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Create navigation frame with home button
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        self.home_button = ctk.CTkButton(
            self.nav_frame,
            text="🏠",
            width=40,
            height=40,
            fg_color="#ffff4d",
            text_color="black",
            hover_color="#e6e600"
        )
        self.home_button.grid(row=0, column=0, padx=10, pady=10)

        # Mode selection buttons
        self.mode_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        self.mode_frame.grid(row=0, column=1, padx=20)
        
        self.intensity_button = ctk.CTkButton(
            self.mode_frame,
            text="INTENSITY MANIPULATION",
            font=("Arial", 24),
            fg_color="transparent",
            text_color="#666666",  # Dimmed text color
            hover_color="#2b2b2b",
            command=lambda: self.switch_mode("intensity")
        )
        self.intensity_button.grid(row=0, column=0, padx=20)

        self.filters_button = ctk.CTkButton(
            self.mode_frame,
            text="FILTERS",
            font=("Arial", 24),
            fg_color="transparent",
            text_color="white",  # Active text color
            hover_color="#2b2b2b",
            command=lambda: self.switch_mode("filters")
        )
        self.filters_button.grid(row=0, column=1, padx=20)

        # Create filter buttons frame
        self.filter_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        self.filter_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        # Create dictionaries for different mode buttons
        self.filter_buttons = ["Sharpen", "Smooth", "Edge Detection", "Emboss", "Gaussian Blur"]
        self.intensity_buttons = ["Brightness", "Contrast", "Saturation", "Exposure", "Highlights", "Shadows"]
        
        self.current_mode = "filters"
        self.current_buttons = []
        self.create_mode_buttons(self.filter_buttons)

        # Create main content frame for images
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.content_frame.grid_columnconfigure((0, 1), weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Create image frames
        self.original_frame = ctk.CTkFrame(self.content_frame, fg_color="#3b3b3b")
        self.original_frame.grid(row=0, column=0, padx=10, sticky="nsew")

        self.edited_frame = ctk.CTkFrame(self.content_frame, fg_color="#3b3b3b")
        self.edited_frame.grid(row=0, column=1, padx=10, sticky="nsew")

        # Create bottom control frame
        self.control_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.control_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=20)

        # Control buttons
        buttons = [
            ("Upload Image", self.upload_image),
            ("Delete Image", self.delete_image),
            ("Undo", self.undo_action),
            ("Redo", self.redo_action),
            ("Save Image", self.save_image)
        ]

        # Add EasyEdits label
        self.logo_label = ctk.CTkLabel(
            self.control_frame,
            text="EasyEdits",
            font=("Arial", 24, "bold")
        )
        self.logo_label.pack(side="left", padx=20)

        # Add control buttons
        for text, command in buttons:
            btn = ctk.CTkButton(
                self.control_frame,
                text=text,
                fg_color="#ffff4d",
                text_color="black",
                hover_color="#e6e600",
                height=35,
                command=command  # Set the button command here
            )
            btn.pack(side="left" if text != "Save Image" else "right", padx=10)

    def create_mode_buttons(self, buttons):
        # Clear existing buttons
        for button in self.current_buttons:
            button.destroy()
        self.current_buttons.clear()

        # Create new buttons
        for i, text in enumerate(buttons):
            btn = ctk.CTkButton(
                self.filter_frame,
                text=text,
                fg_color="transparent",
                hover_color="#3b3b3b",
                command=lambda t=text: self.apply_filter(t)  # Add command to apply the respective filter
            )
            btn.grid(row=0, column=i, padx=10, pady=10)
            self.current_buttons.append(btn)

    def switch_mode(self, mode):
        self.current_mode = mode
        
        # Update button appearances
        if mode == "filters":
            self.filters_button.configure(text_color="white")
            self.intensity_button.configure(text_color="#666666")
            self.create_mode_buttons(self.filter_buttons)
        else:
            self.filters_button.configure(text_color="#666666")
            self.intensity_button.configure(text_color="white")
            self.create_mode_buttons(self.intensity_buttons)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )

        if file_path:
            self.current_image = Image.open(file_path)
            self.original_image = self.current_image.copy()  # Store original image
            self.display_image(self.current_image, self.original_frame)  # Display in original frame
            self.save_history()

    def delete_image(self):
        # Clear the original and edited image frames
        for widget in self.original_frame.winfo_children():
            widget.destroy()
        for widget in self.edited_frame.winfo_children():
            widget.destroy()

        # Reset image variables
        self.current_image = None
        self.original_image = None
        self.history.clear()
        self.redo_history.clear()

    def display_image(self, img, frame):
        for widget in frame.winfo_children():
            widget.destroy()  # Clear existing widgets in the frame
        if img:
            img_tk = ImageTk.PhotoImage(img)
            label = ctk.CTkLabel(frame, image=img_tk)
            label.image = img_tk  # Keep a reference to avoid garbage collection
            label.pack()

    def save_history(self):
        if self.current_image is not None:
            self.history.append(self.current_image.copy())
            self.redo_history.clear()  # Clear redo history after a new action

    def undo_action(self):
        if len(self.history) > 1:
            self.redo_history.append(self.history.pop())  # Move the current image to redo stack
            self.current_image = self.history[-1]  # Set current image to the last one in history
            self.display_image(self.current_image, self.edited_frame)  # Display in edited frame

    def redo_action(self):
        if self.redo_history:
            self.current_image = self.redo_history.pop()  # Move the last undone image back to history
            self.history.append(self.current_image)  # Add it back to the history
            self.display_image(self.current_image, self.edited_frame)  # Display in edited frame

    def save_image(self):
        if self.current_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.current_image.save(file_path)
                print(f"Image saved to {file_path}")

    def apply_filter(self, filter_type):
        if self.current_image is None:
            return
        
        if filter_type == "Sharpen":
            filtered_image = self.current_image.filter(ImageFilter.SHARPEN)
        elif filter_type == "Smooth":
            filtered_image = self.current_image.filter(ImageFilter.SMOOTH)
        elif filter_type == "Edge Detection":
            filtered_image = self.current_image.filter(ImageFilter.FIND_EDGES)
        elif filter_type == "Emboss":
            filtered_image = self.current_image.filter(ImageFilter.EMBOSS)
        elif filter_type == "Gaussian Blur":
            filtered_image = self.current_image.filter(ImageFilter.GaussianBlur(radius=5))
        
        self.current_image = filtered_image
        self.display_image(self.current_image, self.edited_frame)  # Display in edited frame
        self.save_history()  # Save to history after applying the filter

if __name__ == "__main__":
    app = ImageEditorApp()
    app.mainloop()
