import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance, ImageOps

class ImageEditor:
    def __init__(self):
        # Set up the main window
        self.root = ctk.CTk()
        self.root.title("Image Editor")
        self.root.geometry("1200x800")
        self.root.configure(fg_color="#1a1a1a")

        self.current_image = None  # Store current image for editing
        self.original_image = None  # Store original image for reset purposes
        self.history = []  # Store history for undo
        self.redo_history = []  # Store redo actions

        # Create main container
        self.main_container = ctk.CTkFrame(self.root, fg_color="#1a1a1a")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Top navigation frame
        self.nav_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.nav_frame.pack(fill="x", pady=(0, 20))

        # Home button
        self.home_btn = ctk.CTkButton(
            self.nav_frame,
            text="🏠",
            width=50,
            height=50,
            corner_radius=25,
            fg_color="#ffff80",
            text_color="black",
            hover_color="#e6e673"
        )
        self.home_btn.pack(side="left")

        # Section buttons
        self.section_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        self.section_frame.pack(side="left", padx=20)

        self.intensity_btn = ctk.CTkButton(
            self.section_frame,
            text="INTENSITY MANIPULATION",
            font=("Arial", 24, "bold"),
            fg_color="transparent",
            text_color="white",
            hover_color="#2a2a2a"
        )
        self.intensity_btn.pack(side="left", padx=10)

        # Filters button (no change here)
        self.filters_btn = ctk.CTkButton(
            self.section_frame,
            text="FILTERS",
            font=("Arial", 24, "bold"),
            fg_color="transparent",
            text_color="#4d4d4d",
            hover_color="#2a2a2a",
            command=self.open_filters
        )
        self.filters_btn.pack(side="left", padx=10)

        # Action buttons (Upload, Delete, Undo, Redo)
        self.action_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.action_frame.pack(fill="x", pady=(0, 20))

        actions = [
            ("Upload Image", self.upload_image),
            ("Delete Image", self.delete_image),
            ("Undo", self.undo_action),
            ("Redo", self.redo_action)
        ]
        for action_text, action_command in actions:
            btn = ctk.CTkButton(
                self.action_frame,
                text=action_text,
                font=("Arial", 14),
                fg_color="#ffff80",
                text_color="black",
                hover_color="#e6e673",
                height=35,
                corner_radius=20,
                command=action_command
            )
            btn.pack(side="left", padx=5)

        # Easy Edits label
        self.easy_edits_label = ctk.CTkLabel(
            self.action_frame,
            text="EasyEdits",
            font=("Arial", 32, "bold"),
            text_color="white"
        )
        self.easy_edits_label.pack(side="left", padx=20)

        # Save button
        self.save_btn = ctk.CTkButton(
            self.action_frame,
            text="Save Image",
            font=("Arial", 14),
            fg_color="#ffff80",
            text_color="black",
            hover_color="#e6e673",
            height=35,
            corner_radius=20,
            command=self.save_image
        )
        self.save_btn.pack(side="right", padx=5)

        # Image preview frames
        self.preview_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.preview_frame.pack(fill="both", expand=True)

        self.original_frame = ctk.CTkFrame(self.preview_frame, fg_color="#2d2d2d")
        self.original_frame.pack(side="left", fill="both", expand=True, padx=5)

        self.edited_frame = ctk.CTkFrame(self.preview_frame, fg_color="#2d2d2d")
        self.edited_frame.pack(side="right", fill="both", expand=True, padx=5)

        # Controls frame
        self.controls_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.controls_frame.pack(fill="x", pady=(20, 0))

        # Color balancing frame
        self.color_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.color_frame.pack(side="left", fill="x", expand=True)

        self.color_label = ctk.CTkLabel(
            self.color_frame,
            text="Color Balancing",
            font=("Arial", 16),
            text_color="white"
        )
        self.color_label.pack()

        # RGB sliders
        self.red_slider = self.create_slider(self.color_frame, "Red", self.apply_adjustments)
        self.green_slider = self.create_slider(self.color_frame, "Green", self.apply_adjustments)
        self.blue_slider = self.create_slider(self.color_frame, "Blue", self.apply_adjustments)

        # Adjustment frame
        self.adjust_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.adjust_frame.pack(side="right", fill="x", expand=True)

        # Adjustment sliders
        self.brightness_slider = self.create_slider(self.adjust_frame, "Brightness", self.apply_adjustments)
        self.contrast_slider = self.create_slider(self.adjust_frame, "Contrast", self.apply_adjustments)
        self.gamma_slider = self.create_slider(self.adjust_frame, "Gamma", self.apply_adjustments)
        self.negative_slider = self.create_slider(self.adjust_frame, "Negative", self.apply_adjustments)

        # Flag to prevent multiple history saves during slider adjustments
        self.is_adjusting = False

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )

        if file_path:
            self.current_image = Image.open(file_path).convert("RGB")
            self.original_image = self.current_image.copy()  # Store original image
            self.display_image(self.current_image, self.original_frame)  # Display in original frame
            self.display_image(None, self.edited_frame)  # Clear edited frame
            self.history.clear()
            self.redo_history.clear()
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
            # Resize image to fit the frame while maintaining aspect ratio
            frame_width = frame.winfo_width() or 400
            frame_height = frame.winfo_height() or 400
            img_ratio = img.width / img.height
            frame_ratio = frame_width / frame_height

            if img_ratio > frame_ratio:
                new_width = frame_width
                new_height = int(frame_width / img_ratio)
            else:
                new_height = frame_height
                new_width = int(frame_height * img_ratio)

            resized_img = img.resize((new_width, new_height), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(resized_img)
            label = ctk.CTkLabel(frame, image=img_tk)
            label.image = img_tk  # Keep a reference to avoid garbage collection
            label.pack(expand=True)

    def save_history(self):
        if self.current_image is not None:
            self.history.append(self.current_image.copy())
            self.redo_history.clear()  # Clear redo history after a new action

    def undo_action(self):
        if len(self.history) > 1:
            self.redo_history.append(self.history.pop())  # Move the current image to redo stack
            self.current_image = self.history[-1]  # Set current image to the last one in history
            self.display_image(self.current_image, self.edited_frame)  # Display in edited frame
        else:
            print("No more actions to undo.")

    def redo_action(self):
        if self.redo_history:
            self.history.append(self.redo_history.pop())  # Move the last undone image back to history
            self.current_image = self.history[-1]  # Set current image to the one restored
            self.display_image(self.current_image, self.edited_frame)  # Display in edited frame
        else:
            print("No more actions to redo.")

    def save_image(self):
        if self.current_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg *.jpeg"),
                                                                ("All files", "*.*")])
            if file_path:
                self.current_image.save(file_path)
                print(f"Image saved to {file_path}")

    def open_filters(self):
        print("Filters functionality will be implemented here.")

    def create_slider(self, frame, label_text, command):
        label = ctk.CTkLabel(frame, text=label_text, font=("Arial", 16), text_color="white")
        label.pack()
        slider = ctk.CTkSlider(
            frame, from_=0, to=100, width=200, progress_color="#ffff80",
            button_color="#ffff80", button_hover_color="#e6e673", command=lambda v: self.on_slider_change(command)
        )
        slider.set(50)  # Set default to 50 (neutral)
        slider.pack(pady=5)
        return slider

    def on_slider_change(self, command):
        if not self.is_adjusting:
            self.is_adjusting = True
            self.root.after(100, self.perform_adjustments, command)

    def perform_adjustments(self, command):
        command()
        self.save_history()
        self.is_adjusting = False

    def apply_adjustments(self):
        if self.current_image is None:
            return

        # Reset the image to the original for fresh adjustments
        adjusted_image = self.original_image.copy()

        # Apply color balancing
        red_factor = self.red_slider.get() / 50
        green_factor = self.green_slider.get() / 50
        blue_factor = self.blue_slider.get() / 50
        channels = adjusted_image.split()
        adjusted_image = Image.merge(
            "RGB",
            (channels[0].point(lambda i: min(max(i * red_factor, 0), 255)),
             channels[1].point(lambda i: min(max(i * green_factor, 0), 255)),
             channels[2].point(lambda i: min(max(i * blue_factor, 0), 255)))
        )

        # Apply brightness
        brightness_factor = self.brightness_slider.get() / 50
        adjusted_image = ImageEnhance.Brightness(adjusted_image).enhance(brightness_factor)

        # Apply contrast
        contrast_factor = self.contrast_slider.get() / 50
        adjusted_image = ImageEnhance.Contrast(adjusted_image).enhance(contrast_factor)

        # Apply gamma
        gamma_factor = self.gamma_slider.get() / 50
        if gamma_factor != 0:
            adjusted_image = adjusted_image.point(lambda i: 255 * ((i / 255) ** (1 / gamma_factor)))

        # Apply negative (inversion)
        negative_factor = self.negative_slider.get() / 50
        if negative_factor > 1:
            adjusted_image = ImageOps.invert(adjusted_image)

        self.current_image = adjusted_image
        self.display_image(self.current_image, self.edited_frame)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    editor = ImageEditor()
    editor.run()
