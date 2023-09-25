import tkinter as tk

from tkinter import messagebox
import subprocess
import boto3
import tkinter.filedialog as filedialog
import requests
from PIL import Image, ImageTk
import os
import re
import cv2
import time
import webbrowser
import tkinter.simpledialog as simpledialog
import mediapipe as mp

import numpy as np

from tkinter import ttk
import pywhatkit as py
import Integrator

def do_something():
    messagebox.showinfo("Info", "Hi there I am an Tech enthusiast")

def system_app():
    system_window = tk.Toplevel(root)
    system_window.title("System Apps")
    system_window.geometry("400x375")
    system_window.configure(bg="lightgray")
    
    system_label = tk.Label(system_window, text="System Apps", font=("Arial", 20,))
    system_label.pack(pady=10)

    notepad_button = tk.Button(system_window, text="Open Notepad", width=25, fg='Black', command=open_notepad)
    notepad_button.pack(pady=10)

    calculator_button = tk.Button(system_window, text="Open Calculator", width=25, fg='Black', command=open_calculator)
    calculator_button.pack(pady=10)
    
    explorer_button= tk.Button(system_window, text="Explorer", width=25, command=open_explorer)
    explorer_button.pack(pady=10)
    
    custom_button = tk.Button(system_window, text = "Custom", width=25, command=lambda: type_custom_command(system_window))
    custom_button.pack(pady=10)
    
    close_button = tk.Button(system_window, text="Close",width=25, command=system_window.destroy)
    close_button.pack(pady=10)

def on_exit():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

def open_notepad():
    subprocess.Popen("notepad.exe")

def open_calculator():
    subprocess.Popen("calc.exe")
    
def open_explorer():
    subprocess.Popen("explorer.exe")

def type_custom_command(system_window):
    window = tk.Toplevel(system_window)
    window.geometry("250x220")
    Txtbox = tk.Text(window, height = 5, width = 52)
    l = tk.Label(window, text = "Enter the command")
    l.config(font =("Courier", 14))
    print(Txtbox.get("1.0","end"))
    Txtbox.pack()
    # Create button for next text.
    b1 = tk.Button(window, text = "Next", command= lambda: subprocess.getoutput("start "+Txtbox.get("1.0","end")) )
 
    # Create an Exit button.
    b2 = tk.Button(window, text = "close",
            command = window.destroy)
    
    l.pack()
    b1.pack()
    b2.pack()
    
def capture_video():
    if messagebox.askyesno("Exit", "Want to Capture ?"):
        cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter("captured_video.avi", fourcc, 20.0, (640, 480))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

        cv2.imshow("Video", frame)
        if cv2.waitKey(27):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    messagebox.showinfo("Video Captured", "Video captured and saved as 'captured_video.avi'")
    
def aws_operations_window():
    aws_window = tk.Toplevel(root)
    aws_window.title("AWS Operations")
    aws_window.geometry("400x380")
    aws_window.configure(bg="lightgray")
    
    aws_label = tk.Label(aws_window, text="AWS Operations", font=("Arial", 20, "bold"))
    aws_label.pack(pady=10)

    ec2_button = tk.Button(aws_window, text="Create EC2 Instance",width=25, command=open_ec2_instance)
    ec2_button.pack(pady=15)

    s3_button = tk.Button(aws_window, text="Create S3 Bucket",width=25, command=create_s3_bucket)
    s3_button.pack(pady=15)
    
    s3_button = tk.Button(aws_window, text="Upload to S3",width=25, command=upload_to_s3)
    s3_button.pack(pady=15)
    
    list_ec2_button = tk.Button(aws_window, text="List EC2 Instances", width=25, command=list_ec2_instances)
    list_ec2_button.pack(pady=15)

    close_button = tk.Button(aws_window, text="Close",width=25, command=aws_window.destroy)
    close_button.pack(pady=10)
    
def open_ec2_instance():
    response = messagebox.askyesno("AWS EC2 Instance", "Do you want to create an EC2 instance?")
    if response:
        myec2 = boto3.client("ec2")
        response = myec2.run_instances(  
            ImageId='ami-0ded8326293d3201b', 
            InstanceType='t2.micro',
            MaxCount=1,
            MinCount=1
        )
        messagebox.showinfo(title="Output",message=response)

def create_s3_bucket():
    response = messagebox.askyesno("AWS S3 Bucket", "Do you want to create an S3 bucket?")
    if response:
        s3 = boto3.client('s3')
        s3 = s3.create_bucket(
            Bucket='arpit230709845',
            ACL='private',
            CreateBucketConfiguration={
                'LocationConstraint': 'ap-south-1'
            }
        )
        messagebox.showinfo(title="Bucket created successfully",message=response+" was created in the 'ap-south-1' region.")
        
def upload_to_s3():
    bucket_name = simpledialog.askstring("Upload to S3 Bucket", "Enter the bucket name:")
    if bucket_name:
        file_path = filedialog.askopenfilename(title="Select a file to upload")
        if file_path:
            try:
                s3 = boto3.client("s3")
                file_name = os.path.basename(file_path)
                s3.upload_file(file_path, bucket_name, file_name)
                messagebox.showinfo("Upload Successful", f"File '{file_name}' uploaded to '{bucket_name}'")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload file: {e}")
                
def list_ec2_instances():
    try:
        ec2 = boto3.client("ec2")
        response = ec2.describe_instances()
        instances = response["Reservations"]

        if not instances:
            messagebox.showinfo("No EC2 Instances", "No EC2 instances found.")
        else:
            instance_info = "\n".join([f"ID: {instance['Instances'][0]['InstanceId']}, "
                                       f"State: {instance['Instances'][0]['State']['Name']}"
                                       for instance in instances])
            messagebox.showinfo("EC2 Instances", f"List of EC2 instances:\n{instance_info}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to list EC2 instances: {e}")
        
def open_youtube():
    song_name = simpledialog.askstring("Open YouTube", "Enter the name of your favorite song:")
    if song_name:
        search_query = song_name.replace(" ", "+")
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        
def google_search():
    search_query = simpledialog.askstring("Google Search", "Enter your search query:")
    if search_query:
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        
def swap_image():
    import cv2
    try:
    # Load the images
        image = cv2.imread(filedialog.askopenfilename(title="Select the first Image file"))
        image2 = cv2.imread(filedialog.askopenfilename(title="Select Select The second Image File"))

    # Perform the face swap
        image[40:200, 130:300] = image2[70:230, 130:300]
    
    # Display the image with swapped face
        cv2.imshow("Face Swapped Image", image)
        cv2.waitKey()
        cv2.destroyAllWindows()
    except Exception as e:
        messagebox.showerror("Error", f"The prgram crashed Contact support at mymailid@company.com: {e}")
        
def object_detection():
   

    def detect_labels(image_path):
        aws_access_key = 'Optional'
        aws_secret_key = 'Optional'
        client = boto3.client('rekognition', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name='ap-south-1')
        with open(image_path, 'rb') as image_file:
            image_bytes = image_file.read()
        response = client.detect_labels(Image={'Bytes': image_bytes})
        return response['Labels']
    
    def main():
        image_path = 'Messireal.jpg'
        labels = detect_labels(image_path)
    
        print("Labels in the image:")
        for label in labels:
            print(f"- {label['Name']} (Confidence: {label['Confidence']:.2f}%)")

    if __name__ == "__main__":
        main()
        
def whatsapp_message():
    py.sendwhatmsg_instantly("Your number", "Hello, this is an instant WhatsApp message sent using pywhatkit!" )

def wrapper():
    Integrator.input()


root = tk.Tk()
root.title("PyMenu")
root.geometry("1200x750")
root.configure(bg="#f2dfdf")
title_font = ("Sans-serif", 24)
root.iconbitmap(r"logo.ico")




# Welcome Text
title_label = tk.Label(root, text="Python Menu", font=title_font, fg="black")
title_label.grid(row=0 , column=0 ,padx=20 , pady=40)
title_label['bg'] = '#f2dfdf'


system_button = tk.Button(root, text="System Apps", width=25, fg='Black', bg='White', font='sans-serif 11 bold', command=system_app)
system_button.grid(row=1 , column=0 ,padx=20 , pady=20)
capture_video_button = tk.Button(root, text="Capture Video", width=25, bg='White', font='sans-serif 11 bold', command=capture_video)
capture_video_button.grid(row=1 , column=1 ,padx=20 , pady=20)
aws_button = tk.Button(root, text="AWS Operations", width=25, bg='White', font='sans-serif 11 bold', command=aws_operations_window)
aws_button.grid(row=1 , column=2 ,padx=20 , pady=20)

browser_button = tk.Button(root, text="Youtube", width=25, bg='White', font='sans-serif 11 bold', command=open_youtube)
browser_button.grid(row=2 , column=0 ,padx=20 , pady=20)

google_button = tk.Button(root, text="Google Search", width=25, bg='White', font='sans-serif 11 bold',  command=google_search)
google_button.grid(row=2 , column=1 ,padx=30 , pady=20)


Image_swaping_button = tk.Button(root, text="Swap two Images", width=25,bg='White', font='sans-serif 11 bold', command=swap_image)
Image_swaping_button.grid(row=2 , column=2 ,padx=30 , pady=20)


object_detection_button= tk.Button(root, text="Object Detection", width=25, bg='White', font='sans-serif 11 bold', command=object_detection)
object_detection_button.grid(row=3 , column=0 ,padx=30 , pady=20)

deployment_button = tk.Button(root, text="Deploy code writen by ChatGPT", width=27,   bg='White', font='sans-serif 11 bold', command=  wrapper  )
deployment_button.grid(row=3, column=1, padx=30 , pady=20)    
whatsapp_button= tk.Button(root, text="Messenger", width=25,bg='White', font='sans-serif 11 bold', command=whatsapp_message)
whatsapp_button.grid(row=3 , column=2 ,padx=30 , pady=20)



button = tk.Button(root, text="Exit",width=50, bg='White', font='sans-serif 16 bold', command=on_exit)
button.grid(row=4 , columnspan=3 ,padx=30 , pady=20)




# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create a file menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Exit", command=on_exit)
menu_bar.add_cascade(label="File", menu=file_menu)
# Create a help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Info", command=do_something)
menu_bar.add_cascade(label="About", menu=help_menu)



# Start the Tkinter event loop

root.mainloop()
