import tkinter as tk
from PIL import Image, ImageDraw, ImageOps
import numpy as np
import tensorflow as tf
import os
import matplotlib.pyplot as plt


image = Image.new('L', (300, 300), "black")
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
    old_x, old_y = None, None


def draw(event):
    global old_x, old_y
    if old_x is not None and old_y is not None:
        canvas.create_line(event.x, event.y, old_x, old_y,
                           fill="white", width=8, capstyle=tk.ROUND,  smooth=True)
        d.line([event.x, event.y, old_x, old_y],
               fill="white", width=8, joint='curve')

    old_x, old_y = event.x, event.y


def clear(event):
    canvas.delete("all")
    d.rectangle([0, 0, 300, 300], fill="black")


def predict(event):
    global highest_prediction

    resized = image.resize((64, 64), Image.LANCZOS)
    normalized = np.array(resized) / 255.0

    image_array_channel = np.expand_dims(normalized, axis=-1)
    image_batch = np.expand_dims(image_array_channel, axis=0)

    predictions_raw = model.predict(image_batch, verbose=0).flatten()

    top_3_indices = np.argsort(predictions_raw)[::-1][:3]
    top_3_results = [
        f"{os.listdir('hiragana')[i]} ({predictions_raw[i]*100:.2f}%)" for i in top_3_indices]

    display_text = f"Top 3 Predictions:\n" + "\n".join(top_3_results)
    prediction_label.config(text=display_text)


root = tk.Tk()
root.title("Custom Hiragana CNN Classifier")
root.geometry("400x550")

main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack()
tk.Label(main_frame, text="Custom Hiragana Classifier",
         font=("Arial", 18, "bold"), pady=10).pack()

canvas = tk.Canvas(main_frame, bg="black", height=300,
                   width=300, relief=tk.SUNKEN, borderwidth=1)
canvas.pack(pady=10, padx=10)

button_frame = tk.Frame(main_frame)
button_frame.pack()
clearbtn = tk.Button(button_frame, text="Clear")
clearbtn.pack(side=tk.LEFT, padx=5, pady=10, expand=True, fill=tk.BOTH)
predictbtn = tk.Button(button_frame, text="Predict")
predictbtn.pack(side=tk.LEFT, padx=5, pady=10, expand=True, fill=tk.BOTH)

prediction_label = tk.Label(
    main_frame, text="Draw a character", font=("Arial", 14), pady=10)
prediction_label.pack()

canvas.bind("<ButtonPress-1>", start_draw)
canvas.bind("<ButtonRelease-1>", end_draw)
canvas.bind("<B1-Motion>", draw)
clearbtn.bind("<Button-1>", clear)
predictbtn.bind("<Button-1>", predict)

root.mainloop()
