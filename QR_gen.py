import os
import qrcode
from tkinter import *
from tkinter import messagebox, colorchooser, filedialog

from color_picker import pick_color

background_color = "#292929"
frame_bg_color = "#1F1F1F"
text_color = "#B3B3B3"
qr_fill_color = "#000000"
qr_back_color = "#ffffff"


# Creating the window
win = Tk()
win.title('Kims QR Code Generator')
win.geometry('650x750')
win.config(bg=background_color)


def choose_fill_color():
    global qr_fill_color
    color = pick_color(win, initial_color=qr_fill_color, title="Choose QR color")
    if color:
        qr_fill_color = color
        fillColorLabel.config(text=f"Selected QR color: {qr_fill_color}")


def choose_back_color():
    global qr_back_color
    color = pick_color(win, initial_color=qr_back_color, title="Choose background color")
    if color:
        qr_back_color = color
        backColorLabel.config(text=f"Selected background color: {qr_back_color}")


def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        loc_entry.delete(0, END)
        loc_entry.insert(0, folder_selected)


def generateCode():
    try:
        qr_text = text_entry.get().strip()
        save_location = loc_entry.get().strip().strip('"').strip("'")
        qr_name = name_entry.get().strip()
        qr_size = size_entry.get().strip()

        if not qr_text:
            messagebox.showerror("Error", "Please enter text or a URL.")
            return

        if not save_location:
            messagebox.showerror("Error", "Please choose where to save the qr code.")
            return

        if not qr_name:
            messagebox.showerror("Error", "Please enter a file name.")
            return

        if not qr_size:
            qr_size = 5
        elif not qr_size.isdigit():
            messagebox.showerror("Error", "Size must be a number from 1 to 40.")
            return
        else:
            qr_size = int(qr_size)

        if qr_size < 1 or qr_size > 40:
            messagebox.showerror("Error", "Size must be between 1 and 40.")
            return

        if not os.path.isdir(save_location):
            messagebox.showerror("Error", "The folder does not exist.")
            return

        qr = qrcode.QRCode(version=qr_size, box_size=10, border=1)
        qr.add_data(qr_text)
        qr.make(fit=True)

        img = qr.make_image(fill_color=qr_fill_color, back_color=qr_back_color)

        file_path = os.path.join(save_location, f"{qr_name}.png")
        img.save(file_path)

        messagebox.showinfo("Kims QR Code Generator", f"QR Code saved successfully!\n\nSaved as:\n{file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")


headingFrame = Frame(win, bg=background_color, bd=5)
headingFrame.place(relx=0.15, rely=0.05, relwidth=0.7, relheight=0.1)

headingLabel = Label(headingFrame, text="Kims QR Code generator", bg=frame_bg_color, fg=text_color, font=('FiraMono', 20, 'bold'))
headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

Frame1 = Frame(win, bg=background_color)
Frame1.place(relx=0.1, rely=0.15, relwidth=0.7, relheight=0.15)

label1 = Label(Frame1, text="Enter the text/URL: ", bg=background_color, fg=text_color, font=('FiraMono', 13, 'bold'))
label1.place(relx=0.05, rely=0.1, relheight=0.15)

text_entry = Entry(Frame1, font=('Century 12'))
text_entry.place(relx=0.05, rely=0.35, relwidth=1, relheight=0.25)

Frame2 = Frame(win, bg=background_color)
Frame2.place(relx=0.1, rely=0.30, relwidth=0.7, relheight=0.15)

label2 = Label(Frame2, text="Enter the location to save the QR Code: ", bg=background_color, fg=text_color, font=('FiraMono', 13, 'bold'))
label2.place(relx=0.05, rely=0.1, relheight=0.15)

loc_entry = Entry(Frame2, font=('Century 12'))
loc_entry.place(relx=0.05, rely=0.35, relwidth=0.75, relheight=0.25)

browseButton = Button(Frame2, text='Browse', font=('FiraMono', 10), command=browse_folder)
browseButton.place(relx=0.82, rely=0.35, relwidth=0.18, relheight=0.25)

Frame3 = Frame(win, bg=background_color)
Frame3.place(relx=0.1, rely=0.45, relwidth=0.7, relheight=0.15)

label3 = Label(Frame3, text="Enter the name of the QR Code: ", bg=background_color, fg=text_color, font=('FiraMono', 13, 'bold'))
label3.place(relx=0.05, rely=0.1, relheight=0.15)

name_entry = Entry(Frame3, font=('Century 12'))
name_entry.place(relx=0.05, rely=0.35, relwidth=1, relheight=0.25)

Frame4 = Frame(win, bg=background_color)
Frame4.place(relx=0.1, rely=0.60, relwidth=0.7, relheight=0.12)

label4 = Label(Frame4, text="Enter the size from 1 to 40 with 1 being 21x21: ", bg=background_color, fg=text_color, font=('FiraMono', 13, 'bold'))
label4.place(relx=0.05, rely=0.1, relheight=0.2)

size_entry = Entry(Frame4, font=('Century 12'))
size_entry.place(relx=0.05, rely=0.45, relwidth=0.5, relheight=0.25)
size_entry.insert(0, "1")

Frame5 = Frame(win, bg=background_color)
Frame5.place(relx=0.1, rely=0.73, relwidth=0.7, relheight=0.12)

fillColorButton = Button(Frame5, text='Choose QR color', font=('FiraMono', 11), command=choose_fill_color)
fillColorButton.place(relx=0.05, rely=0.1, relwidth=0.4, relheight=0.3)

backColorButton = Button(Frame5, text='Choose background color', font=('FiraMono', 11), command=choose_back_color)
backColorButton.place(relx=0.55, rely=0.1, relwidth=0.4, relheight=0.3)

fillColorLabel = Label(Frame5, text=f"Selected QR color: {qr_fill_color}", bg=background_color, fg=text_color, font=('FiraMono', 10))
fillColorLabel.place(relx=0.05, rely=0.5)

backColorLabel = Label(Frame5, text=f"Selected background color: {qr_back_color}", bg=background_color, fg=text_color, font=('FiraMono', 10))
backColorLabel.place(relx=0.05, rely=0.75)

button = Button(win, text='Generate Code', font=('FiraMono', 15, 'normal'), command=generateCode)
button.place(relx=0.35, rely=0.9, relwidth=0.25, relheight=0.05)

win.mainloop()