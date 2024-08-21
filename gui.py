# Python program to open the 
# camera in Tkinter 
# Import the libraries, 
# tkinter, cv2, Image and ImageTk 

from tkinter import *
import cv2 
from PIL import Image, ImageTk 

# Define a video capture object 
vid = cv2.VideoCapture(0) 

# Declare the width and height in variables 
width, height = 800, 600

# Set the width and height 
vid.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height) 

# Create a GUI app 
app = Tk() 
app.geometry(f"{width}x{height}")

# Set the background color to black
app.configure(bg='black')

# Bind the app with Escape keyboard to 
# quit app whenever pressed 
app.bind('<Escape>', lambda e: app.quit()) 

# Create a label and display it on app 
label_widget = Label(app, bg='black') 
label_widget.pack()

# Global variable to store the timer ID
camera_update_id = None

# Function to update the camera frame in the label widget
def update_camera_frame():
    global camera_update_id

    # Capture the video frame by frame 
    ret, frame = vid.read() 

    if ret:
        # Convert image from one color space to another 
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 

        # Capture the latest frame and transform to image 
        captured_image = Image.fromarray(opencv_image) 

        # Convert captured image to photoimage 
        photo_image = ImageTk.PhotoImage(image=captured_image) 

        # Displaying photoimage in the label 
        label_widget.photo_image = photo_image 

        # Configure image in the label 
        label_widget.configure(image=photo_image) 

        # Repeat the same process after every 10 milliseconds 
        camera_update_id = label_widget.after(10, update_camera_frame)

# Function to open the camera
def open_camera():
    vid.open(0)
    update_camera_frame()
    button1.config(text="Close Camera", command=close_camera)

# Function to close the camera
def close_camera():
    global camera_update_id

    if camera_update_id is not None:
        label_widget.after_cancel(camera_update_id)
        camera_update_id = None

    # Release the video capture object
    vid.release()

    # Clear the image from the label widget
    label_widget.config(image='')
    button1.config(text="Open Camera", command=open_camera)

# Create a button to open the camera in GUI app 
button1 = Button(app, text="Open Camera", command=open_camera, bg='black', fg='white', font=('Helvetica', 14, 'bold')) 
button1.pack(pady=20) 

# Create an infinite loop for displaying app on screen 
app.mainloop()
