import tkinter as tk
from tkinter import ttk, S, font
from PIL import Image, ImageTk
from barcode import EAN13, ITF
from barcode.writer import ImageWriter
import webbrowser
import sys
from typing import Union, Type

from config import config as cfg


def open_github_url(event=None):
    """ Performs the task of clicking on the link. """
    webbrowser.open_new(r'https://github.com/SSA1MON/barcodes-show')


def about_help_menu():
    """ The About window in the menubar. """
    geometry_w = cfg.menubar.get('help').get('about').get('size').get('w')
    geometry_h = cfg.menubar.get('help').get('about').get('size').get('h')

    about_window = tk.Toplevel(padx=10, pady=10)
    about_window.title(cfg.menubar.get('help').get('about').get('title'))
    about_window.iconbitmap(cfg.favicon)
    about_window.geometry(f'{geometry_w}x{geometry_h}')
    about_window.minsize(geometry_w, geometry_h)
    about_window.maxsize(geometry_w, geometry_h)
    about_window.focus()

    title_label = ttk.Label(about_window, text='Barcodes show', font=('Arial', 14))
    version_label = ttk.Label(about_window, text='dev-beta-build')
    url_label = ttk.Label(
        about_window, text='Github', foreground='#0000EE',
        cursor='hand2', font='Arial 10 underline'
    )
    url_label.bind('<Button-1>', func=open_github_url)

    title_label.pack()
    version_label.pack()
    url_label.pack(expand=True, anchor=S)


def exit_window_menu() -> None:
    """ Shutdown the application. """
    sys.exit(0)


def identify_barcode_type(input_text: str) -> Union[Type[ITF], Type[EAN13], None]:
    """
    Determines the barcode type based on the received value for further generation.
    14 символов = ITF14, 13 символов = EAN13
    Args:
        input_text (str): The value entered by the user
    """
    if input_text.isdigit():
        if len(input_text) == 14:
            return ITF
        elif len(input_text) == 13:
            return EAN13
    return None


# def reset_app_data() -> None:
#     print(default_image)
#     barcode_area.focus()
#     default_barcode.image = cfg.default_image
#     label_barcode_info.config(image=default_barcode, compound='top')
#     error_label.pack_forget()
#     default_barcode.pack_forget()


def generate_barcode(event=None) -> None:
    """
    Generates a barcode based on the entered text and updates the display.
    Args:
        event:
    """
    input_text = barcode_area.get()
    barcode_type = identify_barcode_type(input_text)
    if barcode_type is not None:
        my_barcode = barcode_type(input_text, writer=ImageWriter())
        if barcode_type == ITF:
            img = my_barcode.render(writer_options={'module_width': 0.18})
        else:
            img = my_barcode.render()
        img = ImageTk.PhotoImage(img)

        error_label.pack_forget()
        label_barcode_info.pack()
        label_barcode_info.config(text='Тип: ' + str(barcode_type))
        default_barcode.image = img
        default_barcode.config(image=default_barcode.image)

        barcode_area.delete(0, tk.END)
        barcode_area.focus()
    else:
        error_label.pack()
        error_label.config(
            text=cfg.barcode_err_text, font=('Verdana', 12),
            background='#d9534f', foreground='white'
        )
        barcode_area.delete(0, tk.END)
        barcode_area.focus()
        label_barcode_info.pack_forget()
        default_barcode.config(image=default_image)


# root window settings
window = tk.Tk()
window.title(cfg.window.get('title'))
window.iconbitmap(cfg.favicon)
window.geometry(cfg.window.get('size'))
window.minsize(cfg.window.get('minsize').get('w'), cfg.window.get('minsize').get('h'))
window.maxsize(cfg.window.get('maxsize').get('w'), cfg.window.get('maxsize').get('h'))
window.config(background='white')

# menu bar
menubar = tk.Menu(window)
window_menu = tk.Menu(menubar, tearoff=0)
help_menu = tk.Menu(menubar, tearoff=0)
help_menu.winfo_geometry()

# two-level menu
menubar.add_cascade(label='Window', menu=window_menu)
window_menu.add_command(label='Exit', command=exit_window_menu)
menubar.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='About', command=about_help_menu)

# label for image
default_image = Image.open(cfg.default_image)
default_image = ImageTk.PhotoImage(default_image)
default_barcode = ttk.Label(
    image=default_image, compound='top', font=('Arial', 1), background='white'
)
default_barcode.pack()

frame = tk.Frame(master=window, background='white')
frame.pack(expand=True)

# entry
barcode_area = tk.Entry(frame, width=40)
barcode_area.grid(row=1, column=2)
barcode_area.bind('<Return>', generate_barcode)     # bind for the Enter button
barcode_area.focus()

# buttons
btn_style = ttk.Style().configure('TButton', background='white', font=('Arial', 11))
gen_btn = ttk.Button(frame, text='Сгенерировать', command=generate_barcode, padding=7, width=28)
# reset_btn = ttk.Button(frame, text='Сброс', command=reset_app_data, padding=7, width=28)
gen_btn.grid(row=2, column=2, pady=(10, 2))
# reset_btn.grid(row=3, column=2)

# label in the footer
error_label = ttk.Label(background='white')
error_label.pack()

# information in the footer about the class of the entered barcode (for dev)
label_barcode_info = ttk.Label(foreground='#D5CABD', background='white')
label_barcode_info.pack()


if __name__ == '__main__':
    window.config(menu=menubar)
    window.mainloop()
