# QR Code Generator 🎨

A user-friendly QR code generator built with Python and Tkinter.
This application allows you to create customizable QR codes with advanced color selection, including a custom-built color picker.

---

## ✨ Features

* Generate QR codes from text or URLs
* Save QR codes as PNG files
* Custom file name and save location
* Adjustable QR code size
* Adjustable border size
* Advanced color customization:

  * 🎨 Visual gradient color picker (HSV)
  * 🔢 HEX input
  * 🔴 RGB input
  * 🎯 Preset color palette
* Modern GUI built with Tkinter

---

## 🖥️ Preview

Creates QR codes like this:

* Custom colors
* Adjustable styling
* Clean and minimal output

---

## 📦 Installation

### 1. Clone or download the project

```bash
git clone <your-repo-url>
cd QR_code_generator
```

or download as ZIP and extract.

---

### 2. Install dependencies

```bash
pip install qrcode[pil]
pip install pillow
```

---

## ▶️ Run the program

```bash
python QR_gen.py
```

---

## ⚙️ Usage

1. Enter text or a URL
2. Choose where to save the file
3. Enter a file name
4. Adjust size and border
5. Pick colors using the color picker
6. Click **Generate Code**

---

## 🎨 Color Picker

The project includes a custom-built color picker module:

* Gradient-based color selection (HSV)
* Manual HEX input (#RRGGBB)
* Manual RGB input (0–255)
* Live preview
* Preset color palette

File:

```
fancy_color_picker.py
```

---

## 📁 Project Structure

```
QR_code_generator/
│
├── QR_gen.py               # Main application
├── fancy_color_picker.py  # Custom color picker module
└── README.md
```


---

## ⚠️ Notes

* For best QR scanning results:

  * Use high contrast between foreground and background
  * Avoid very small borders
* Recommended:

  * Dark QR + light background

---

## 🚀 Future Improvements

* Display QR preview inside GUI
* Export to SVG
* Add logo inside QR code
* Save favorite colors

---

## 👨‍💻 Author

Kim H. Thorsen

---

