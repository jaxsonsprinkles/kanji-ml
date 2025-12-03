import tkinter as tk
from PIL import Image, ImageDraw
import numpy as np
import tensorflow as tf
import os

image = Image.new('L', (300,300), "white")
d = ImageDraw.Draw(image)
old_x = None
old_y = None
model = tf.keras.models.load_model('hiragana_model.keras')
highest_prediction = ""
def start_draw(event):
    global old_x, old_y
    old_x, old_y = event.x, event.y

def end_draw(event):
    global old_x, old_y
    old_x = None
    old_y = None
    
    
def draw(event):
    global old_x, old_y
    if old_x is not None and old_y is not None:
        # Create a line on the canvas and Pillow image
        canvas.create_line(event.x, event.y, old_x, old_y, fill="black", width=4, capstyle=tk.ROUND,  smooth=True)  
        d.line([event.x, event.y, old_x, old_y], fill="black", width=4, joint='curve')
    old_x, old_y = event.x, event.y

def clear(event):
   canvas.delete("all")
   d.rectangle([0,0,300,300], fill="white")

def predict(event):
   global highest_prediction

   # Resize and normalize image
   resized = image.resize((64,64), Image.LANCZOS)
   normalized = np.array(resized)/255.0
   
   # Add extra dimensions for tf model
   image_array_channel = np.expand_dims(normalized, axis=-1)
   image_batch = np.expand_dims(image_array_channel, axis=0)
   
   # Load model and predict image
   predictions = model.predict(image_batch)
   highest_prediction = os.listdir('hiragana')[np.argmax(predictions[0])]
   prediction_label.config(text=f"Highest Prediction:{highest_prediction} ")


# Initialize window
root = tk.Tk()
root.title("Hiragana CNN")
root.geometry("800x800")

# Create elements
main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.grid(row=0, column=0)
tk.Label(main_frame, text="Hiragana CNN Classifier", font=("Arial", 18, "bold"), pady=10).grid(row=0, column=0, columnspan=2)
canvas = tk.Canvas(main_frame, bg="white", height=300, width=300, relief=tk.SUNKEN, borderwidth=1)
canvas.grid(row=1, column=0, columnspan=2, pady=10, padx=10)
clearbtn = tk.Button(main_frame, text="Clear")
clearbtn.grid(row=2, column=0, padx=5, pady=10, sticky=tk.EW)
predictbtn = tk.Button(main_frame, text="Predict")
predictbtn.grid(row=2, column=1, padx=5, pady=10, sticky=tk.EW)
prediction_label = tk.Label(main_frame, text="Draw a character", font=("Arial", 14), pady=10)
prediction_label.grid(row=3, column=0, columnspan=2)
# Bind actions to functions
canvas.bind("<ButtonPress-1>", start_draw)
canvas.bind("<ButtonRelease-1>", end_draw)
canvas.bind("<B1-Motion>", draw)
clearbtn.bind("<Button-1>", clear)
predictbtn.bind("<Button-1>", predict)

root.mainloop()