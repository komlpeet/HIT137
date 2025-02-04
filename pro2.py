import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Canvas, Label, Button, Scale, HORIZONTAL
from PIL import Image, ImageTk

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        
        self.image = None
        self.cropped_image = None
        self.resized_cropped_image = None
        self.start_x = self.start_y = self.end_x = self.end_y = 0
        self.drawing = False
        
        self.load_button = Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack()
        
        self.canvas = Canvas(root, width=500, height=500, bg="gray")
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        self.crop_button = Button(root, text="Crop Image", command=self.crop_image)
        self.crop_button.pack()
        
        self.resize_label = Label(root, text="Resize Slider")
        self.resize_label.pack()
        
        self.resize_slider = Scale(root, from_=50, to=200, orient=HORIZONTAL, command=self.resize_image)
        self.resize_slider.pack()
        
        self.save_button = Button(root, text="Save Image", command=self.save_image)
        self.save_button.pack()
        
    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.display_image(self.image)
    
    def display_image(self, img):
        img = cv2.resize(img, (500, 500))
        img = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(img)
        self.canvas.image = img_tk
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    
    def on_mouse_down(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.drawing = True
    
    def on_mouse_drag(self, event):
        if self.drawing:
            self.end_x, self.end_y = event.x, event.y
            self.canvas.delete("crop_rect")
            self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline="red", tag="crop_rect")
    
    def on_mouse_up(self, event):
        self.drawing = False
    
    def crop_image(self):
        if self.image is not None and self.start_x and self.start_y and self.end_x and self.end_y:
            self.cropped_image = self.image[self.start_y:self.end_y, self.start_x:self.end_x]
            self.resized_cropped_image = self.cropped_image.copy()
            self.display_cropped_image()
    
    def display_cropped_image(self):
        if self.resized_cropped_image is not None:
            img = Image.fromarray(self.resized_cropped_image)
            img_tk = ImageTk.PhotoImage(img)
            self.canvas.create_image(250, 250, anchor=tk.NW, image=img_tk)
            self.canvas.image = img_tk
    
    def resize_image(self, val):
        if self.cropped_image is not None:
            factor = int(val)
            new_width = int(self.cropped_image.shape[1] * factor / 100)
            new_height = int(self.cropped_image.shape[0] * factor / 100)
            self.resized_cropped_image = cv2.resize(self.cropped_image, (new_width, new_height))
            self.display_cropped_image()
    
    def save_image(self):
        if self.resized_cropped_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg"),
                                                                ("All Files", "*.*")])
            if file_path:
                cv2.imwrite(file_path, cv2.cvtColor(self.resized_cropped_image, cv2.COLOR_RGB2BGR))
                print("Image saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()
