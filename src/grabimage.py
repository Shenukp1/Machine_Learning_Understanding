#Original Author: Jonathan Hudson
#CPSC 433 F24
"""
File contains a way to produce 28x28 images of letter for the model to predict.
"""

import os
from tkinter import *
from tkinter import simpledialog, messagebox
from PIL import Image, ImageDraw
from constant import IMAGE_DIR

#State of mouse
b1 = "up"
canvas_img = Image.new("L", (28*8, 28*8), 255)
canvas_draw = ImageDraw.Draw(canvas_img)

def b1down(event):
    global b1
    b1 = "down"
def b1up(event):
    global b1
    b1 = "up"
def motion(event):
    if b1 == "down":
        event.widget.create_oval(event.x,event.y,event.x,event.y, width=16)
        r = 8
        canvas_draw.ellipse((event.x - r, event.y - r, event.x + r, event.y + r), fill=0)

VALID_NAMES = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J"}

def save_image(img):
    """QoL - Allows me to create more images and not overwrite them.
    """
    os.makedirs(IMAGE_DIR, exist_ok=True)
    name = simpledialog.askstring("Save Image", "Enter a capital letter (A-J):")
    if name not in VALID_NAMES:
        messagebox.showerror("Invalid Name", "Save failed: Name must be a capital letter from A to J.")
        return
    # TODO(shenukp1) Nov 13, 2026: I dont really see a need for multiple so we shall overwrite for now
    filepath = os.path.join(IMAGE_DIR, f"{name}.png")
    img.resize((28, 28)).save(filepath)
    print(f"Saved {filepath}")

# Main to draw window, capture buttons events, and save image
def main():
    root = Tk()
    root.title("Draw")
    drawing_area = Canvas(root,bg="white",width=28*8,height=28*8)
    drawing_area.pack()
    drawing_area.bind("<Motion>", motion)
    drawing_area.bind("<ButtonPress-1>", b1down)
    drawing_area.bind("<ButtonRelease-1>", b1up)
    button=Button(root,fg="green",text="Save",command=lambda:getter(canvas_img))
    button.pack(side=LEFT)
    button=Button(root,fg="green",text="Clear",command=lambda:delete(drawing_area))
    button.pack(side=RIGHT)
    def delete(widget):
        widget.delete("all")
        canvas_draw.rectangle((0, 0, 28*8, 28*8), fill=255)
    def getter(img):
        save_image(img)
    root.mainloop()
  
if __name__ == "__main__":
    main()
