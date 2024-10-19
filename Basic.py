import customtkinter as ctk
from PIL import Image, ImageTk, ImageOps, ImageFilter
import tkinter as tk
from tkinter import filedialog


class ImageEditor:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Basic EasyEdits")
        self.app.geometry("1200x800")
        self.app._set_appearance_mode("dark")
        
        self.current_image = None  # Store current image for editing
        self.original_image = None  # Store original image for reset purposes
        self.history = []  # Store history for undo
        self.redo_history = []  # Store redo actions
        self.current_angle = 0  # Track the current rotation angle
        self.horizontal_flipped = False  # Track horizontal flip state
        self.vertical_flipped = False  # Track vertical flip state
        self.current_image = None  # Store current image for editing


        # Configure grid
        self.app.grid_columnconfigure(1, weight=1)
        self.app.grid_rowconfigure(1, weight=1)

        # Create header frame
        self.header_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=(20,0), sticky="ew")

        # Home button with redirection to GetStart interface
        self.home_btn = ctk.CTkButton(
            self.header_frame,
            text="🏠",
            width=50,
            height=50,
            corner_radius=25,
            fg_color="#ffff4d",
            text_color="black",
            command=self.go_home
        )
        self.home_btn.grid(row=0, column=0, padx=(0, 20))

        # Title
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Basic",
            font=ctk.CTkFont(size=40, weight="bold")
        )
        self.title_label.grid(row=0, column=1)

        # Top buttons frame
        self.top_buttons_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.top_buttons_frame.grid(row=0, column=2, padx=20)

        # Top buttons
        buttons = ["Upload Image", "Delete Image", "Undo", "Redo", "EasyEdits", "Save Image"]
        for i, text in enumerate(buttons):
            if text == "EasyEdits":
                label = ctk.CTkLabel(
                    self.top_buttons_frame,
                    text=text,
                    font=ctk.CTkFont(size=24, weight="bold")
                )
                label.grid(row=0, column=i, padx=10)
            else:
                btn = ctk.CTkButton(
                    self.top_buttons_frame,
                    text=text,
                    fg_color="#ffff4d" if text != "Undo" and text != "Redo" else "gray30",
                    text_color="black",
                    corner_radius=20,
                    command=self.get_button_action(text)
                )
                btn.grid(row=0, column=i, padx=5)

        # Image frames
        self.left_image_frame = ctk.CTkFrame(self.app, fg_color="gray30")
        self.left_image_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.right_image_frame = ctk.CTkFrame(self.app, fg_color="gray30")
        self.right_image_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        # Controls frame
        self.controls_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        self.controls_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        # Rotate controls
        self.rotate_label = ctk.CTkLabel(self.controls_frame, text="Rotate Image")
        self.rotate_label.grid(row=0, column=0, padx=(0, 10))

        self.rotate_slider = ctk.CTkSlider(self.controls_frame, width=200, from_=0, to=360, command=self.rotate_image)
        self.rotate_slider.grid(row=0, column=1, padx=10)

        # Center buttons
        self.invert_btn = ctk.CTkButton(
            self.controls_frame,
            text="Invert Colors",
            fg_color="gray30",
            corner_radius=20,
            command=self.invert_colors
        )
        self.invert_btn.grid(row=0, column=2, padx=20)

        self.edge_btn = ctk.CTkButton(
            self.controls_frame,
            text="Edge Detection",
            fg_color="gray30",
            corner_radius=20,
            command=self.edge_detection
        )
        self.edge_btn.grid(row=0, column=3, padx=20)

        # Flip options
        self.horizontal_cb = ctk.CTkCheckBox(self.controls_frame, text="Flip Horizontal", command=self.flip_horizontal)
        self.horizontal_cb.grid(row=0, column=4)

        self.vertical_cb = ctk.CTkCheckBox(self.controls_frame, text="Flip Vertical", command=self.flip_vertical)
        self.vertical_cb.grid(row=0, column=5, padx=10)


        # Crop frame
        self.crop_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        self.crop_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")

        self.crop_label = ctk.CTkLabel(self.crop_frame, text="Crop Image")
        self.crop_label.grid(row=0, column=0, padx=10)

        # Crop coordinates entries
        coords = ["X1", "X2", "Y1", "Y2"]
        self.crop_entries = {}
        for i, coord in enumerate(coords):
            entry = ctk.CTkEntry(
                self.crop_frame,
                placeholder_text=coord,
                width=100,
                fg_color="gray30"
            )
            entry.grid(row=0, column=i + 1, padx=10)
            self.crop_entries[coord] = entry

        # Filter buttons
        self.bw_btn = ctk.CTkButton(
            self.crop_frame,
            text="Black & White",
            fg_color="gray30",
            corner_radius=20,
            command=self.convert_to_bw
        )
        self.bw_btn.grid(row=0, column=5, padx=10)

        self.grayscale_btn = ctk.CTkButton(
            self.crop_frame,
            text="Grayscale",
            fg_color="gray30",
            corner_radius=20,
            command=self.convert_to_gray
        )
        self.grayscale_btn.grid(row=0, column=6, padx=10)

    def go_home(self):
        self.app.destroy()
        from GetStart import EasyEditsApp
        app = EasyEditsApp()
        app.mainloop()

    def get_button_action(self, text):
        if text == "Upload Image":
            return self.upload_image
        elif text == "Delete Image":
            return self.delete_image
        elif text == "Undo":
            return self.undo_action
        elif text == "Redo":
            return self.redo_action
        elif text == "Save Image":
            return self.save_image

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.current_image = Image.open(file_path)
            self.original_image = self.current_image.copy()  # Store original image
            self.current_image.thumbnail((400, 400))
            self.display_image(self.current_image, self.left_image_frame)
            self.save_history()

    def display_image(self, image, frame):
        img_tk = ImageTk.PhotoImage(image)
        label = ctk.CTkLabel(frame, image=img_tk)
        label.grid(row=0, column=0, padx=20, pady=20)
        frame.image = img_tk  # Keep a reference to prevent garbage collection

    def invert_colors(self):
        if self.current_image:
            inverted_image = ImageOps.invert(self.current_image.convert("RGB"))
            self.display_image(inverted_image, self.right_image_frame)
            self.save_history(inverted_image)

    def edge_detection(self):
        if self.current_image:
            edge_image = self.current_image.filter(ImageFilter.FIND_EDGES)
            self.display_image(edge_image, self.right_image_frame)
            self.save_history(edge_image)

    def flip_horizontal(self):
        if self.current_image:
            self.horizontal_flipped = not self.horizontal_flipped  # Toggle the flip state
            flipped_image = self.current_image.transpose(Image.FLIP_LEFT_RIGHT) if self.horizontal_flipped else self.current_image
            self.display_image(flipped_image, self.right_image_frame)
            self.save_history(flipped_image)

    def flip_vertical(self):
        if self.current_image:
            self.vertical_flipped = not self.vertical_flipped  # Toggle the flip state
            flipped_image = self.current_image.transpose(Image.FLIP_TOP_BOTTOM) if self.vertical_flipped else self.current_image
            self.display_image(flipped_image, self.right_image_frame)
            self.save_history(flipped_image)


    def convert_to_bw(self):
        if self.current_image:
            bw_image = self.current_image.convert("1")
            self.display_image(bw_image, self.right_image_frame)
            self.save_history(bw_image)

    def convert_to_gray(self):
        if self.current_image:
            gray_image = self.current_image.convert("L")
            self.display_image(gray_image, self.right_image_frame)
            self.save_history(gray_image)

    def rotate_image(self, angle):
        if self.original_image:
            rotated_image = self.original_image.rotate(angle, expand=True)
            self.current_image = rotated_image
            self.display_image(self.current_image, self.right_image_frame)
            self.save_history(rotated_image)

    def crop_image(self):
        if self.current_image:
            try:
                x1, x2 = int(self.crop_entries["X1"].get()), int(self.crop_entries["X2"].get())
                y1, y2 = int(self.crop_entries["Y1"].get()), int(self.crop_entries["Y2"].get())
                cropped_image = self.current_image.crop((x1, y1, x2, y2))
                self.display_image(cropped_image, self.right_image_frame)
                self.save_history(cropped_image)
            except ValueError:
                print("Invalid crop coordinates")

    def save_image(self):
        if self.current_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.current_image.save(file_path)
                print(f"Image saved to {file_path}")

    def delete_image(self):
        # Clear the left image frame
        for widget in self.left_image_frame.winfo_children():
            widget.destroy()

        self.current_image = None  # Set current image to None or handle as needed
        self.display_image(None, self.right_image_frame)  # Clear the displayed image
        
        # Clear the right image frame
        for widget in self.right_image_frame.winfo_children():
            widget.destroy()

        # Reset image variables
        self.current_image = None
        self.original_image = None
        self.history.clear()
        self.redo_history.clear()

    def save_history(self, img=None):
        if img is None:
            img = self.current_image
        self.history.append(img)
        self.redo_history.clear()  # Clear redo history after a new action

    def undo_action(self):
        if len(self.history) > 1:
            self.redo_history.append(self.history.pop())  # Move the current image to redo stack
            self.current_image = self.history[-1]  # Set current image to the last one in history
            # Check and apply flips
            if self.horizontal_flipped:
                self.current_image = self.current_image.transpose(Image.FLIP_LEFT_RIGHT)
            if self.vertical_flipped:
                self.current_image = self.current_image.transpose(Image.FLIP_TOP_BOTTOM)
        self.display_image(self.current_image, self.right_image_frame)

    def redo_action(self):
        if self.redo_history:
            self.history.append(self.redo_history.pop())  # Move the last undone image back to history
            self.current_image = self.history[-1]  # Set current image to the one restored
            self.display_image(self.current_image, self.right_image_frame)

    def run(self):
        self.app.mainloop()


if __name__ == "__main__":
    editor = ImageEditor()
    editor.run()
