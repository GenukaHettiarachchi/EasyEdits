import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter
import numpy as np
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image

# Initialize ResNet50 model
model = ResNet50(weights='imagenet')

# Create a basic window
app = ctk.CTk()
app.title("Easy Edits")
app.geometry("1000x800")

uploaded_image = None
processed_image = None

# Function to upload and display an image
def upload_image():
    global uploaded_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    if file_path:
        uploaded_image = Image.open(file_path)
        img = uploaded_image.resize((400, 300), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        upload_image_label.configure(image=img_tk)
        upload_image_label.image = img_tk  # Keep reference to avoid garbage collection

def sharpen_image():
    global processed_image, uploaded_image
    if uploaded_image:
        # Apply sharpening filter
        processed_image = uploaded_image.filter(ImageFilter.SHARPEN)
        img = processed_image.resize((400, 300), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        processed_image_label.configure(image=img_tk)
        processed_image_label.image = img_tk  # Keep reference to avoid garbage collection

def save_image():
    global processed_image
    if processed_image:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", ".png"), ("JPEG files", ".jpg"), ("BMP files", "*.bmp")])
        if file_path:
            processed_image.save(file_path)

# Function to perform dog identification using ResNet50
def identify_dog_breed():
    global uploaded_image
    if uploaded_image:
        # Convert PIL image to format acceptable for ResNet50
        img = uploaded_image.resize((224, 224))
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        # Predict using ResNet50 model
        preds = model.predict(img_array)
        predictions = decode_predictions(preds, top=3)[0]
        
        # Display prediction result
        result_text = f"1. {predictions[0][1]} ({predictions[0][2]*100:.2f}% confidence)\n" \
                      f"2. {predictions[1][1]} ({predictions[1][2]*100:.2f}% confidence)\n" \
                      f"3. {predictions[2][1]} ({predictions[2][2]*100:.2f}% confidence)"
        result_label.configure(text=result_text)

# Function to perform simple image segmentation based on identified object
def segment_image():
    global uploaded_image, processed_image
    if uploaded_image:
        # Placeholder segmentation logic: For demonstration, we just resize the image.
        processed_image = uploaded_image.filter(ImageFilter.CONTOUR)  # Example segmentation effect
        img = processed_image.resize((400, 300), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        processed_image_label.configure(image=img_tk)
        processed_image_label.image = img_tk  # Keep reference to avoid garbage collection

# Button to upload the image
upload_button = ctk.CTkButton(app, text="Upload Image", command=upload_image)
upload_button.pack(pady=20)

# Label to display the uploaded image
upload_image_label = ctk.CTkLabel(app, text="No image uploaded yet.")
upload_image_label.pack(pady=10)

# Label to display the processed image
processed_image_label = ctk.CTkLabel(app, text="No processed image yet.")
processed_image_label.pack(pady=10)

# Button to sharpen the image
sharpen_button = ctk.CTkButton(app, text="Sharpen Image", command=sharpen_image)
sharpen_button.pack(pady=10)

# Button to identify the dog breed using ResNet50
identify_button = ctk.CTkButton(app, text="Identify Dog Breed", command=identify_dog_breed)
identify_button.pack(pady=10)

# Label to display the identification result
result_label = ctk.CTkLabel(app, text="No prediction yet.")
result_label.pack(pady=10)

# Button to segment the image (placeholder logic)
segment_button = ctk.CTkButton(app, text="Segment Image", command=segment_image)
segment_button.pack(pady=10)

# Button to save the processed image
save_button = ctk.CTkButton(app, text="Save Image", command=save_image)
save_button.pack(pady=20)

# Run the app
app.mainloop()