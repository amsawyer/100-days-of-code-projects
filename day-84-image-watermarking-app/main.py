from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image, ImageFont, ImageDraw
import math


GRAY = (211, 211, 211, 128)
BLUE = '#035397'
out_img = None
img_filename = ''
FONT_RATIO = 3.2
DIAGONAL_PERCENTAGE = 0.5
WIDTH_PERCENTAGE = 0.8
WIDTH = 200
HEIGHT = 200


def open_filename():
    """
    Open filesystem dialog to allow user to select file for upload.
    """
    filename = filedialog.askopenfilename(title="Upload")
    return filename


def download_img():
    """
    Save watermarked image to user's local filesystem.
    """
    # Download watermarked image
    out_img.save(f"Watermarked_{img_filename}")
    img_downloaded_label.grid(row=2)


def upload_img():
    """
    Get uploaded image, add watermark, and save image for download.
    """
    global out_img
    global img_filename
    global watermark_img
    global canvas_wm_img

    # get image uploaded by user
    img_name = open_filename()
    # get uploaded image name (part of path after last '/')
    img_filename = img_name.split('/')[-1]
    watermark_text = watermark_input.get()
    if watermark_text == "":
        watermark_text = " "
    wm_text_length = len(watermark_text)

    # Clear existing items off of canvas
    watermark_label.grid_forget()
    watermark_input.grid_forget()
    upload_label.grid_forget()
    upload_btn.grid_forget()

    # Watermark added success message
    img_uploaded_label.grid(row=0)

    # Display Download button
    download_btn.grid(row=1)
    # Display "Watermark Another Image" button
    watermark_another_btn.grid(row=3)

    with Image.open(img_name).convert("RGBA") as base:
        # Dynamically determine best font size to use
        diagonal_length = base.size[0] * WIDTH_PERCENTAGE
        diagonal_to_use = diagonal_length * DIAGONAL_PERCENTAGE
        font_size = int(diagonal_to_use / (wm_text_length / FONT_RATIO))
        font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", font_size)
        wm_width, wm_height = font.getsize(watermark_text)
        # Create watermark overlay with transparent background
        watermark_overlay = Image.new("RGBA", (wm_width, wm_height), (0, 0, 0, 0))

        # Write watermark text supplied by user
        draw = ImageDraw.Draw(watermark_overlay)
        draw.text((0, 0), text=watermark_text, font=font, fill=GRAY)
        # Dynamically determine best rotation angle to use
        angle = math.degrees(math.atan(base.size[1] / base.size[0]))
        # Rotate the watermark to diagonal angle
        watermark_overlay = watermark_overlay.rotate(angle, expand=1)

        wx, wy = watermark_overlay.size
        px = int((base.size[0] - wx) / 2)
        py = int((base.size[1] - wy) / 2)
        # Paste watermark overlay over base uploaded image
        base.paste(watermark_overlay, (px, py, px + wx, py + wy), watermark_overlay)
        # Convert image back to RGB format so it can be displayed in the app
        watermark_img = ImageTk.PhotoImage(base.convert("RGB"))

        # Display image with watermark added
        canvas.config(width=base.size[0] * 1.1, height=base.size[1] * 1.1)
        canvas.itemconfig(canvas_image, image="")
        canvas_wm_img = canvas.create_image(base.size[0] * 1.1 / 2, base.size[1] * 1.1 / 2, image=watermark_img)
        canvas.grid(row=4)

        # Save base image as global var so it can be downloaded
        out_img = base


def display_upload_ui():
    """
    Display initial welcome / upload screen of UI.
    """
    # Resize canvas back to starting size
    canvas.config(width=WIDTH, height=HEIGHT)
    # Clear existing items off of canvas
    canvas.delete(canvas_wm_img)
    img_uploaded_label.grid_forget()
    download_btn.grid_forget()
    img_downloaded_label.grid_forget()
    watermark_another_btn.grid_forget()

    # Display components of initial welcome / upload screen
    canvas.itemconfig(canvas_image, image=logo_img) # Display Watermarker logo
    canvas.grid(column=0, row=0, columnspan=3)
    watermark_label.grid(column=1, row=1)
    watermark_input.grid(column=2, row=1)
    upload_label.grid(column=0, row=2, columnspan=3)
    upload_btn.grid(column=0, row=3, columnspan=3)


window = Tk()
window.title("Watermarker - Image Watermarking App")
window.config(padx=50, pady=50)
window.resizable(width=True, height=True)
canvas = Canvas(width=WIDTH, height=HEIGHT)

# PhotoImages must be defined outside of a function
logo_img = PhotoImage(file="images/logo.gif")
watermark_img = None
canvas_wm_img = None

# Watermarker logo image
canvas_image = canvas.create_image(100, 100, image=logo_img)

# Display welcome text
watermark_label = Label(text="Watermark to add to image: ")
watermark_input = Entry(width=25)
watermark_input.insert(0, "Confidential")
upload_label = Label(text="Click the button below to upload your image.")

# Upload button
upload_btn_img = PhotoImage(file="images/upload.gif")
upload_btn = Button(window,
                    image=upload_btn_img,
                    command=upload_img)
# Watermark added success message
img_uploaded_label = Label(text="Watermark added successfully. "
                                "Click the button below to download the watermarked image.")
# Download button
download_btn_img = PhotoImage(file="images/download.gif")
download_btn = Button(window,
                      image=download_btn_img,
                      command=download_img)
img_downloaded_label = Label(text="Image downloaded to current working directory!",
                             fg=BLUE)
# Watermark Another Image button (redirects back to initial upload UI)
watermark_another_btn = Button(window,
                               text="Watermark Another Image",
                               command=display_upload_ui,
                               highlightbackground=BLUE)
display_upload_ui()


window.mainloop()
