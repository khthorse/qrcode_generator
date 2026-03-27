import tkinter as tk
from tkinter import Toplevel, messagebox
import colorsys
from PIL import Image, ImageTk


def hex_to_rgb(hex_color):
    hex_color = hex_color.strip().lstrip("#")
    if len(hex_color) != 6:
        raise ValueError("HEX color must have 6 characters.")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    return f"#{r:02X}{g:02X}{b:02X}"


def rgb_to_hsv(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return h, s, v


def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)


def clamp(value, min_value=0, max_value=255):
    return max(min_value, min(max_value, value))


class FancyColorPicker:
    def __init__(self, parent, initial_color="#000000", title="Choose Color"):
        self.parent = parent
        self.initial_color = initial_color
        self.title = title
        self.selected_color = None
        self.updating = False

        try:
            r, g, b = hex_to_rgb(initial_color)
        except Exception:
            r, g, b = 0, 0, 0

        self.h, self.s, self.v = rgb_to_hsv(r, g, b)

        self.sv_width = 256
        self.sv_height = 256
        self.hue_width = 30
        self.hue_height = 256

        self.sv_photo = None
        self.hue_photo = None

    def show(self):
        self.window = Toplevel(self.parent)
        self.window.title(self.title)
        self.window.geometry("520x680")
        self.window.resizable(False, False)
        self.window.configure(bg="#f2f2f2")
        self.window.grab_set()

        title_label = tk.Label(
            self.window,
            text=self.title,
            font=("Segoe UI", 16, "bold"),
            bg="#f2f2f2"
        )
        title_label.pack(pady=(12, 8))

        top_frame = tk.Frame(self.window, bg="#f2f2f2")
        top_frame.pack(pady=8)

        self.sv_canvas = tk.Canvas(
            top_frame,
            width=self.sv_width,
            height=self.sv_height,
            bd=1,
            relief="sunken",
            highlightthickness=0
        )
        self.sv_canvas.pack(side="left", padx=(0, 12))

        self.hue_canvas = tk.Canvas(
            top_frame,
            width=self.hue_width,
            height=self.hue_height,
            bd=1,
            relief="sunken",
            highlightthickness=0
        )
        self.hue_canvas.pack(side="left")

        self.sv_canvas.bind("<Button-1>", self.on_sv_click)
        self.sv_canvas.bind("<B1-Motion>", self.on_sv_click)

        self.hue_canvas.bind("<Button-1>", self.on_hue_click)
        self.hue_canvas.bind("<B1-Motion>", self.on_hue_click)

        self.preview = tk.Label(
            self.window,
            text="Preview",
            font=("Segoe UI", 12, "bold"),
            width=20,
            height=3,
            relief="ridge",
            bd=2
        )
        self.preview.pack(pady=12)

        hex_frame = tk.Frame(self.window, bg="#f2f2f2")
        hex_frame.pack(pady=6)

        tk.Label(
            hex_frame,
            text="HEX:",
            font=("Segoe UI", 11, "bold"),
            bg="#f2f2f2"
        ).pack(side="left", padx=(0, 8))

        self.hex_entry = tk.Entry(hex_frame, font=("Consolas", 12), width=12, justify="center")
        self.hex_entry.pack(side="left")
        self.hex_entry.bind("<KeyRelease>", self.on_hex_change)

        rgb_input_frame = tk.Frame(self.window, bg="#f2f2f2")
        rgb_input_frame.pack(pady=10)

        tk.Label(rgb_input_frame, text="R:", font=("Segoe UI", 11, "bold"), bg="#f2f2f2").grid(row=0, column=0, padx=(0, 5))
        self.r_entry = tk.Entry(rgb_input_frame, width=5, justify="center", font=("Consolas", 11))
        self.r_entry.grid(row=0, column=1, padx=(0, 12))
        self.r_entry.bind("<KeyRelease>", self.on_rgb_change)

        tk.Label(rgb_input_frame, text="G:", font=("Segoe UI", 11, "bold"), bg="#f2f2f2").grid(row=0, column=2, padx=(0, 5))
        self.g_entry = tk.Entry(rgb_input_frame, width=5, justify="center", font=("Consolas", 11))
        self.g_entry.grid(row=0, column=3, padx=(0, 12))
        self.g_entry.bind("<KeyRelease>", self.on_rgb_change)

        tk.Label(rgb_input_frame, text="B:", font=("Segoe UI", 11, "bold"), bg="#f2f2f2").grid(row=0, column=4, padx=(0, 5))
        self.b_entry = tk.Entry(rgb_input_frame, width=5, justify="center", font=("Consolas", 11))
        self.b_entry.grid(row=0, column=5)
        self.b_entry.bind("<KeyRelease>", self.on_rgb_change)

        rgb_frame = tk.Frame(self.window, bg="#f2f2f2")
        rgb_frame.pack(pady=8)

        self.r_label = tk.Label(rgb_frame, text="R: 0", font=("Segoe UI", 10), bg="#f2f2f2")
        self.r_label.pack(side="left", padx=8)

        self.g_label = tk.Label(rgb_frame, text="G: 0", font=("Segoe UI", 10), bg="#f2f2f2")
        self.g_label.pack(side="left", padx=8)

        self.b_label = tk.Label(rgb_frame, text="B: 0", font=("Segoe UI", 10), bg="#f2f2f2")
        self.b_label.pack(side="left", padx=8)

        presets_frame = tk.Frame(self.window, bg="#f2f2f2")
        presets_frame.pack(pady=(8, 12))

        preset_colors = [
            "#000000", "#FFFFFF", "#B2B3B7", "#FFFEA7", "#3E31D6", "#86A4F7", 
            "#E6ECFF", "#2EC483", "#6CE1AB", "#CEFFDF", "#B60000", "#DD0000", 
            "#FB6666", "#FEE0E0", "#FEA11B", "#FDCB87", "#FFE8D4", "#2e6bf6"
        ]

        for i, color in enumerate(preset_colors):
            row = i // 10
            col = i % 10

            tk.Button(
                presets_frame,
                bg=color,
                width=3,
                command=lambda c=color: self.set_from_hex(c)
            ).grid(row=row, column=col, padx=3, pady=3)

        button_frame = tk.Frame(self.window, bg="#f2f2f2")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="OK",
            font=("Segoe UI", 11, "bold"),
            width=10,
            command=self.confirm
        ).pack(side="left", padx=8)

        tk.Button(
            button_frame,
            text="Cancel",
            font=("Segoe UI", 11),
            width=10,
            command=self.cancel
        ).pack(side="left", padx=8)

        self.draw_hue_bar()
        self.update_from_hsv(redraw_sv=True)

        self.window.wait_window()
        return self.selected_color

    def draw_hue_bar(self):
        img = Image.new("RGB", (self.hue_width, self.hue_height))
        pixels = img.load()

        for y in range(self.hue_height):
            h = y / (self.hue_height - 1)
            r, g, b = hsv_to_rgb(h, 1, 1)
            for x in range(self.hue_width):
                pixels[x, y] = (r, g, b)

        self.hue_photo = ImageTk.PhotoImage(img)
        self.hue_canvas.delete("all")
        self.hue_canvas.create_image(0, 0, anchor="nw", image=self.hue_photo)
        self.draw_hue_marker()

    def draw_sv_gradient(self):
        img = Image.new("RGB", (self.sv_width, self.sv_height))
        pixels = img.load()

        for x in range(self.sv_width):
            s = x / (self.sv_width - 1)
            for y in range(self.sv_height):
                v = 1 - (y / (self.sv_height - 1))
                r, g, b = hsv_to_rgb(self.h, s, v)
                pixels[x, y] = (r, g, b)

        self.sv_photo = ImageTk.PhotoImage(img)
        self.sv_canvas.delete("all")
        self.sv_canvas.create_image(0, 0, anchor="nw", image=self.sv_photo)

        x = int(self.s * (self.sv_width - 1))
        y = int((1 - self.v) * (self.sv_height - 1))
        self.draw_sv_marker(x, y)

    def draw_sv_marker(self, x, y):
        self.sv_canvas.delete("marker")
        self.sv_canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="white", width=2, tags="marker")
        self.sv_canvas.create_oval(x - 6, y - 6, x + 6, y + 6, outline="black", width=1, tags="marker")

    def draw_hue_marker(self):
        self.hue_canvas.delete("marker")
        y = int(self.h * (self.hue_height - 1))
        self.hue_canvas.create_rectangle(
            0, y - 2, self.hue_width, y + 2,
            outline="white", width=2, tags="marker"
        )
        self.hue_canvas.create_rectangle(
            1, y - 3, self.hue_width - 1, y + 3,
            outline="black", width=1, tags="marker"
        )

    def update_from_hsv(self, redraw_sv=False):
        r, g, b = hsv_to_rgb(self.h, self.s, self.v)
        hex_color = rgb_to_hex(r, g, b)

        self.updating = True

        if redraw_sv:
            self.draw_sv_gradient()
        else:
            x = int(self.s * (self.sv_width - 1))
            y = int((1 - self.v) * (self.sv_height - 1))
            self.draw_sv_marker(x, y)

        self.draw_hue_marker()

        self.preview.config(bg=hex_color, text=hex_color)
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        self.preview.config(fg="black" if brightness > 128 else "white")

        self.hex_entry.delete(0, tk.END)
        self.hex_entry.insert(0, hex_color)

        self.r_entry.delete(0, tk.END)
        self.r_entry.insert(0, str(r))
        self.g_entry.delete(0, tk.END)
        self.g_entry.insert(0, str(g))
        self.b_entry.delete(0, tk.END)
        self.b_entry.insert(0, str(b))

        self.r_label.config(text=f"R: {r}")
        self.g_label.config(text=f"G: {g}")
        self.b_label.config(text=f"B: {b}")

        self.updating = False

    def on_hue_click(self, event):
        y = max(0, min(self.hue_height - 1, event.y))
        self.h = y / (self.hue_height - 1)
        self.update_from_hsv(redraw_sv=True)

    def on_sv_click(self, event):
        x = max(0, min(self.sv_width - 1, event.x))
        y = max(0, min(self.sv_height - 1, event.y))

        self.s = x / (self.sv_width - 1)
        self.v = 1 - (y / (self.sv_height - 1))
        self.update_from_hsv(redraw_sv=False)

    def on_hex_change(self, event=None):
        if self.updating:
            return

        value = self.hex_entry.get().strip()
        if not value:
            return

        if not value.startswith("#"):
            value = "#" + value

        if len(value) != 7:
            return

        try:
            r, g, b = hex_to_rgb(value)
            self.h, self.s, self.v = rgb_to_hsv(r, g, b)
            self.update_from_hsv(redraw_sv=True)
        except Exception:
            pass

    def on_rgb_change(self, event=None):
        if self.updating:
            return

        r_text = self.r_entry.get().strip()
        g_text = self.g_entry.get().strip()
        b_text = self.b_entry.get().strip()

        if not r_text or not g_text or not b_text:
            return

        if not (r_text.isdigit() and g_text.isdigit() and b_text.isdigit()):
            return

        r = clamp(int(r_text))
        g = clamp(int(g_text))
        b = clamp(int(b_text))

        self.h, self.s, self.v = rgb_to_hsv(r, g, b)
        self.update_from_hsv(redraw_sv=True)

    def set_from_hex(self, hex_color):
        try:
            r, g, b = hex_to_rgb(hex_color)
            self.h, self.s, self.v = rgb_to_hsv(r, g, b)
            self.update_from_hsv(redraw_sv=True)
        except Exception:
            messagebox.showerror("Error", "Invalid color.", parent=self.window)

    def confirm(self):
        value = self.hex_entry.get().strip()
        if not value.startswith("#"):
            value = "#" + value

        try:
            hex_to_rgb(value)
            self.selected_color = value.upper()
            self.window.destroy()
        except Exception:
            messagebox.showerror(
                "Invalid color",
                "Please enter a valid HEX color in the format #RRGGBB.",
                parent=self.window
            )

    def cancel(self):
        self.selected_color = None
        self.window.destroy()


def pick_color(parent, initial_color="#000000", title="Choose Color"):
    picker = FancyColorPicker(parent, initial_color=initial_color, title=title)
    return picker.show()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    color = pick_color(root, initial_color="#00CED1", title="Test Color Picker")
    print("Selected color:", color)
    root.destroy()