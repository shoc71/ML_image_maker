from PIL import Image, ImageDraw
import tkinter as tk
import random
import string
import os

# Constants
CANVAS_WIDTH, CANVAS_HEIGHT = 64, 64
SAVE_SIZE = (64, 64)
SAVE_DIR = "drawings"

os.makedirs(SAVE_DIR, exist_ok=True)

def generate_random_string(length=24):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mock Painter App")

        self.canvas = tk.Canvas(root, bg="white", width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.pack()

        self.undo_button = tk.Button(root, text="Undo", command=self.undo_last)
        self.undo_button.pack(pady=5)

        self.canvas.bind("<Button-1>", self.activate_paint)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.root.bind("<KeyPress-s>", self.save_and_reset_canvas)

        self.init_drawing_surface()
        self.last_x, self.last_y = None, None
        self.strokes = []

    def init_drawing_surface(self):
        self.image = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), "white")
        self.draw = ImageDraw.Draw(self.image)

    def activate_paint(self, event):
        self.last_x, self.last_y = event.x, event.y

    def paint(self, event):
        x, y = event.x, event.y
        if self.last_x is not None and self.last_y is not None:
            self.canvas.create_line(self.last_x, self.last_y, x, y, fill="black", width=3)
            self.draw.line([self.last_x, self.last_y, x, y], fill="black", width=3)
            self.strokes.append((self.last_x, self.last_y, x, y))
        self.last_x, self.last_y = x, y
        
    def print_drawing_count(self):
        files = [f for f in os.listdir(SAVE_DIR) if f.lower().endswith(".png")]
        print(f"\n Total drawings saved: {len(files)} \n")

    def save_and_reset_canvas(self, event=None):
        random_str = generate_random_string()
        filename = f"train_one_{random_str}.png"
        full_path = os.path.join(SAVE_DIR, filename)

        # Resize to 64x64 and save
        try:
            resized_image = self.image.resize(SAVE_SIZE, Image.ANTIALIAS)
        except:
            resized_image = self.image.resize(SAVE_SIZE, Image.Resampling.LANCZOS)
        resized_image.save(full_path)

        print(f"Saved drawing as {full_path} (64x64)")
        
        # Print file count
        self.print_drawing_count()

        self.canvas.delete("all")
        self.init_drawing_surface()
        self.strokes.clear()
        self.last_x, self.last_y = None, None

    def undo_last(self):
        if self.strokes:
            self.strokes.pop()
            self.redraw_from_strokes()

    def redraw_from_strokes(self):
        self.canvas.delete("all")
        self.init_drawing_surface()

        for x1, y1, x2, y2 in self.strokes:
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=3)
            self.draw.line([x1, y1, x2, y2], fill="black", width=3)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()