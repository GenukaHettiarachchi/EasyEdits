import customtkinter as ctk
import cv2
import numpy as np
from PIL import Image, ImageTk
from ultralytics import YOLO

import GetStart

class ModernImageSegmentation:
    def __init__(self):
        self.initialize_model() # Initialize the YOLO model
        self.initialize_gui() # Set up the GUI components
        self.content_image = None # Placeholder for the loaded content image
        self.original_size = None # To store the original size of the image
        self.original_cv_image = None # To store the original image in OpenCV format
        self.processed_image = None  # Add this to store the processed image
        
    def initialize_model(self):
        # Load pre-trained YOLO model
        self.model = YOLO('yolov8x.pt')
        
        # Animal classes in COCO dataset
        self.animal_classes = [
            'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
            'zebra', 'giraffe'
        ]

    def initialize_gui(self):
        # Configure appearance for GUI
        ctk.set_appearance_mode("dark") # Set dark mode appearance
        ctk.set_default_color_theme("dark-blue") # Set color theme to dark blue
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Image Segmentation")
        self.root.geometry("1200x800")

        # Create main container
        container = ctk.CTkFrame(self.root)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header with title
        header = ctk.CTkFrame(container)
        header.pack(fill="x", pady=(0, 20))
        
        # Home button
        home_btn = ctk.CTkButton(
            header, 
            text="🏠",
            width=50,
            fg_color="#FFE169",
            text_color="black",
            hover_color="#FFD700"
        )
        home_btn.pack(side="left", padx=10)

        # Title
        title = ctk.CTkLabel(
            header,
            text="Image Segmentation",
            font=ctk.CTkFont(family="Arial", size=32, weight="bold")
        )
        title.pack(side="left", expand=True)

        # Top button frame
        btn_frame = ctk.CTkFrame(container)
        btn_frame.pack(fill="x", pady=(0, 20))

        # Left side buttons
        left_btns = ctk.CTkFrame(btn_frame)
        left_btns.pack(side="left")

        upload_btn = ctk.CTkButton(
            left_btns,
            text="Upload Image",
            fg_color="#FFE169",
            text_color="black",
            hover_color="#FFD700",
            command=self.load_content_image
        )
        upload_btn.pack(side="left", padx=5)

        # Right side
        right_btns = ctk.CTkFrame(btn_frame)
        right_btns.pack(side="right")

        # EasyEdits label
        easy_edits = ctk.CTkLabel(
            right_btns,
            text="EasyEdits",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        easy_edits.pack(side="left", padx=10)

        save_btn = ctk.CTkButton(
            right_btns,
            text="Save Image",
            fg_color="#FFE169",
            text_color="black",
            hover_color="#FFD700",
            command=self.save_image  # Connect save button to the save function
        )
        save_btn.pack(side="left", padx=5)

        # Image frames container
        image_container = ctk.CTkFrame(container)
        image_container.pack(fill="both", expand=True)

        # Create image frames
        self.content_frame = ctk.CTkFrame(image_container, fg_color="#3F3F3F")
        self.content_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        self.stylized_frame = ctk.CTkFrame(image_container, fg_color="#3F3F3F")
        self.stylized_frame.pack(side="right", fill="both", expand=True, padx=10)

        # Create canvases
        self.content_canvas = ctk.CTkCanvas(
            self.content_frame,
            width=512,
            height=512,
            bg='#3F3F3F',
            highlightthickness=0
        )
        self.content_canvas.pack(expand=True)

        self.stylized_canvas = ctk.CTkCanvas(
            self.stylized_frame,
            width=512,
            height=512,
            bg='#3F3F3F',
            highlightthickness=0
        )
        self.stylized_canvas.pack(expand=True)

        # Detect button at bottom
        detect_btn = ctk.CTkButton(
            container,
            text="Detect Animals",
            fg_color="#FFE169",
            text_color="black",
            hover_color="#FFD700",
            height=40,
            command=self.apply_detection
        )
        detect_btn.pack(pady=20)

        # Animal similarity label
        similarity_label = ctk.CTkLabel(
            container,
            text="",
            font=ctk.CTkFont(size=16)
        )
        similarity_label.pack(pady=10)

    def save_image(self):
        """Save the processed image with animal detection highlights."""
        if self.processed_image is None:
            print("No processed image to save. Please detect animals first.")
            return
            
        try:
            # Open file dialog for saving
            file_path = ctk.filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("All files", "*.*")
                ]
            )
            
            if file_path:
                # Convert the processed image to uint8 format
                save_image = (self.processed_image * 255).astype(np.uint8)
                # Convert to PIL Image
                save_image = Image.fromarray(save_image)
                # Save the image
                save_image.save(file_path)
                print(f"Image saved successfully to {file_path}")
                
        except Exception as e:
            print(f"Failed to save image: {str(e)}")

    def load_image(self, image_path, max_dim=None):
        # Load image with OpenCV
        self.original_cv_image = cv2.imread(image_path)
        self.original_cv_image = cv2.cvtColor(self.original_cv_image, cv2.COLOR_BGR2RGB)
        
        # Store original size
        self.original_size = self.original_cv_image.shape[:2]
        
        # Resize if needed
        if max_dim:
            height, width = self.original_size
            scale = min(max_dim/width, max_dim/height)
            if scale < 1:
                new_width = int(width * scale)
                new_height = int(height * scale)
                self.original_cv_image = cv2.resize(self.original_cv_image, 
                                                  (new_width, new_height))
        
        # Convert to RGB format
        image = Image.fromarray(self.original_cv_image)
        
        return np.array(image).astype(np.float32) / 255.0

    def detect_and_highlight_animal(self, image):
        # Convert float image back to uint8
        image_uint8 = (image * 255).astype(np.uint8)
        
        # Run YOLO detection
        results = self.model(image_uint8)
        
        # Create a mask for animals
        mask = np.zeros(image_uint8.shape[:2], dtype=np.uint8)
        
        # Create a copy of the image for highlighting
        highlighted_image = image.copy()
        
        # Process detection results
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get class name
                class_id = int(box.cls[0].item())
                class_name = result.names[class_id]
                
                # Check if detected object is an animal
                if class_name.lower() in self.animal_classes:
                    # Get coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                    
                    # Create mask for this detection
                    cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)
        
        # Apply highlighting effect
        highlight_color = np.array([1.0, 0.0, 0.0])  # Red color
        alpha = 0.3  # Transparency
        
        # Create highlighted version
        for c in range(3):  # For each color channel
            highlighted_image[..., c] = np.where(mask == 255,
                                               image[..., c] * (1 - alpha) + highlight_color[c] * alpha,
                                               image[..., c])
        
        return highlighted_image

    def display_image(self, image, canvas):
        try:
            # Ensure image is in range [0, 1]
            image = np.clip(image, 0, 1)
            
            # Convert to uint8
            image = (image * 255).astype(np.uint8)
            
            # Create PIL Image
            image = Image.fromarray(image)
            
            # Resize to fit canvas
            canvas_width = int(canvas.winfo_width())
            canvas_height = int(canvas.winfo_height())
            if canvas_width > 1 and canvas_height > 1:
                image = image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Clear canvas and display new image
            canvas.delete("all")
            canvas.create_image(0, 0, anchor="nw", image=photo)
            canvas.image = photo
            
        except Exception as e:
            print(f"Failed to display image: {str(e)}")

    def load_content_image(self):
        try:
            content_image_path = ctk.filedialog.askopenfilename(
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")]
            )
            if content_image_path:
                self.content_image = self.load_image(content_image_path, max_dim=512)
                self.display_image(self.content_image, self.content_canvas)
        except Exception as e:
            print(f"Failed to load image: {str(e)}")

    def apply_detection(self):
        try:
            if self.content_image is None:
                print("Please load an image first")
                return
            
            # Detect and highlight animals
            self.processed_image = self.detect_and_highlight_animal(self.content_image)
            
            # Display result
            self.display_image(self.processed_image, self.stylized_canvas)
            
        except Exception as e:
            print(f"Detection failed: {str(e)}")

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
    app = ModernImageSegmentation()
    app.run()