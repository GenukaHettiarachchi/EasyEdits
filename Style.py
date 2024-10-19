import customtkinter as ctk
import tkinter as tk
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog
import matplotlib.pyplot as plt
from io import BytesIO

import GetStart

class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

class StyleTransferApp:
    def __init__(self, original_window=None):
        # Store reference to original window
        self.original_window = original_window
        
        # Configure appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Create main window
        self.root = ctk.CTk() if original_window is None else ctk.CTkToplevel(original_window)
        self.root.title("Style Transfer")
        
        # Set window size and position it in center
        window_width = 1200
        window_height = 900
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        
        # Set the window size and position
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Make the window resizable
        self.root.resizable(True, True)
        
        # Calculate dimensions for UI elements
        self.image_width = 400
        self.image_height = 300
        self.result_width = 800
        self.result_height = 400
        
        # Create main container frame
        self.create_main_container()
        
        # Initialize image variables
        self.content_image = None
        self.style_image = None
        self.result_image = None
        self.content_photo = None
        self.style_photo = None
        self.result_photo = None

    def create_main_container(self):
        # Create main container frame
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(expand=True, fill="both")
        
        # Create scrollable frame
        self.scrollable_frame = ScrollableFrame(
            self.main_container,
            width=1160,  # Adjust width to account for scrollbar
            height=860,  # Adjust height to account for padding
            fg_color="transparent"
        )
        self.scrollable_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Create and pack header and content inside scrollable frame
        self.create_header()
        self.create_main_content()

    def create_header(self):
        # Header frame
        header_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Home button
        home_button = ctk.CTkButton(
            header_frame, 
            text="🏠", 
            width=40,
            height=40,
            fg_color="#FFE75C",
            hover_color="#FFD700",
            text_color="black",
            command=self.go_to_home
        )
        home_button.pack(side="left", padx=(0, 10))
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame, 
            text="Style Transfer",
            font=("Playfair Display", 36, "bold")
        )
        title_label.pack(side="left", expand=True)
        
        # EasyEdits label
        easy_edits_label = ctk.CTkLabel(
            header_frame,
            text="EasyEdits",
            font=("Inter", 24)
        )
        easy_edits_label.pack(side="right")

    def create_main_content(self):
        # Images section frame
        images_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        images_frame.pack(fill="x", pady=10)
        
        # Content image section
        content_section = ctk.CTkFrame(images_frame, fg_color="transparent")
        content_section.pack(side="left", expand=True, padx=10)
        
        ctk.CTkLabel(content_section, text="Content Image", font=("Inter", 18, "bold")).pack(pady=5)
        self.content_frame = ctk.CTkFrame(content_section, fg_color="#2B2B2B", 
                                        width=self.image_width, height=self.image_height)
        self.content_frame.pack(pady=5)
        self.content_frame.pack_propagate(False)
        
        # Style image section
        style_section = ctk.CTkFrame(images_frame, fg_color="transparent")
        style_section.pack(side="right", expand=True, padx=10)
        
        ctk.CTkLabel(style_section, text="Style Image", font=("Inter", 18, "bold")).pack(pady=5)
        self.style_frame = ctk.CTkFrame(style_section, fg_color="#2B2B2B", 
                                      width=self.image_width, height=self.image_height)
        self.style_frame.pack(pady=5)
        self.style_frame.pack_propagate(False)
        
        # Result section
        result_section = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        result_section.pack(fill="x", pady=20)
        
        ctk.CTkLabel(result_section, text="Result Image", font=("Inter", 18, "bold")).pack(pady=5)
        self.result_frame = ctk.CTkFrame(result_section, fg_color="#2B2B2B", 
                                       width=self.result_width, height=self.result_height)
        self.result_frame.pack(pady=5)
        self.result_frame.pack_propagate(False)
        
        # Buttons section
        buttons_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=20)
        
        # Button style configuration
        button_style = {
            "fg_color": "#FFE75C",
            "text_color": "black",
            "hover_color": "#FFD700",
            "height": 40,
            "font": ("Inter", 14, "bold"),
            "width": 200
        }
        
        # Top row buttons
        top_buttons_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        top_buttons_frame.pack(pady=5)
        
        ctk.CTkButton(
            top_buttons_frame,
            text="Upload Content Image",
            command=self.load_content_image,
            **button_style
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            top_buttons_frame,
            text="Upload Style Image",
            command=self.load_style_image,
            **button_style
        ).pack(side="left", padx=10)
        
        # Bottom row buttons
        bottom_buttons_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        bottom_buttons_frame.pack(pady=5)
        
        ctk.CTkButton(
            bottom_buttons_frame,
            text="Apply Style Transfer",
            command=self.apply_style_transfer,
            **button_style
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            bottom_buttons_frame,
            text="Save Result Image",
            command=self.save_result_image,
            **button_style
        ).pack(side="left", padx=10)

    # [Rest of the methods remain unchanged]
    def load_image(self, image_path, frame_size):
        img = Image.open(image_path)
        img.thumbnail(frame_size)
        img_array = np.array(img)
        normalized_img = tf.image.convert_image_dtype(img_array, tf.float32)
        return normalized_img[tf.newaxis, :], img
    
    def display_image(self, pil_image, frame, frame_size):
        for widget in frame.winfo_children():
            widget.destroy()
        
        img_width, img_height = pil_image.size
        frame_width, frame_height = frame_size
        ratio = min(frame_width/img_width, frame_height/img_height)
        new_size = (int(img_width * ratio), int(img_height * ratio))
        ctk_image = ctk.CTkImage(pil_image, size=new_size)
        image_label = ctk.CTkLabel(frame, image=ctk_image, text="")
        image_label.place(relx=0.5, rely=0.5, anchor="center")
        return ctk_image
    
    def load_content_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ppm *.pgm")]
        )
        if file_path:
            self.content_image, pil_image = self.load_image(file_path, (self.image_width, self.image_height))
            self.content_photo = self.display_image(pil_image, self.content_frame, (self.image_width, self.image_height))
    
    def load_style_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ppm *.pgm")]
        )
        if file_path:
            self.style_image, pil_image = self.load_image(file_path, (self.image_width, self.image_height))
            self.style_photo = self.display_image(pil_image, self.style_frame, (self.image_width, self.image_height))

    def apply_style_transfer(self):
        if self.content_image is not None and self.style_image is not None:
            try:
                hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
                self.result_image = hub_model(tf.constant(self.content_image), tf.constant(self.style_image))[0]
                result_array = np.squeeze(self.result_image.numpy())
                result_array = (result_array * 255).astype(np.uint8)
                pil_image = Image.fromarray(result_array)
                self.result_photo = self.display_image(pil_image, self.result_frame, 
                                                     (self.result_width, self.result_height))
            except Exception as e:
                self.show_message("Error", f"Style transfer failed: {str(e)}")
        else:
            self.show_message("Error", "Please upload both content and style images first!")

    def save_result_image(self):
        if self.result_image is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            if file_path:
                try:
                    image = np.squeeze(self.result_image.numpy())
                    image = (image * 255).astype(np.uint8)
                    image = Image.fromarray(image)
                    image.save(file_path)
                    self.show_message("Success", "Image saved successfully!")
                except Exception as e:
                    self.show_message("Error", f"Failed to save image: {str(e)}")
        else:
            self.show_message("Error", "No result image to save!")

    def show_message(self, title, message):
        dialog = ctk.CTkInputDialog(
            text=message,
            title=title,
            button_text="OK"
        )
        dialog.geometry("300x150")

    def go_to_home(self):
        self.root.destroy()
        if self.original_window:
            self.original_window.deiconify()
        else:
            root = ctk.CTk()
            get_start = GetStart.GetStart(root)
            root.mainloop()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = StyleTransferApp()
    app.run()