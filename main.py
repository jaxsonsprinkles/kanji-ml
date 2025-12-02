import tkinter as tk

old_x = None
old_y = None

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
     canvas.create_line(event.x, event.y, old_x, old_y, fill="black", width=4, capstyle=tk.ROUND,  smooth=True)   
    old_x, old_y = event.x, event.y

def clear(event):
   canvas.delete("all")

def predict(event):
   pass

# Initialize window
root = tk.Tk()
root.title("Hiragana CNN")
root.geometry("600x400")

# Create elements
tk.Label(root, text="Hiragana CNN", font=("Arial", 16, "bold"), padx=15, pady=15).pack()
canvas = tk.Canvas(root, bg="lavender", height=300, width=300)
canvas.pack()
clearbtn = tk.Button(root, text="Clear")
clearbtn.pack()
predictbtn = tk.Button(root, text="Predict")
predictbtn.pack()

# Bind actions to functions
canvas.bind("<ButtonPress-1>", start_draw)
canvas.bind("<ButtonRelease-1>", end_draw)
canvas.bind("<B1-Motion>", draw)
clearbtn.bind("<Button-1>", clear)
predictbtn.bind("<Button-1>", predict)

root.mainloop()