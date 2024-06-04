import tkinter as tk
from tkinter import ttk
import math
import pymysql

root = tk.Tk()
root.title("")

window_width = 800
window_height = 600
root.geometry(f"{window_width}x{window_height}+200+80")

root.resizable(False, False)

max_radius = 110
min_radius = 10

label = tk.Label(root, text="Analysis", fg="black", font=("Helvetica", 30), bg="white")
label.pack()

frame_width = 500
frame_height = 500
frame = tk.Frame(root, width=frame_width, height=frame_height, bd=2, relief="solid", bg="light yellow")
frame.pack(side="left", padx=20)

canvas = tk.Canvas(frame, width=frame_width, height=frame_height, bg="black")
canvas.pack()

center_x = frame_width // 2
center_y = frame_height // 2

num_circles = 11

radius_difference = 10

input_frame = tk.Frame(root, bg="black")
input_frame.pack(side="right", padx=10)

points = []

def redraw_circles():
    canvas.delete("all")
    for i in range(num_circles):
        radius = min_radius + i * radius_difference 
        canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius, outline='red'
        )
    canvas.create_text(center_x, center_y, text='x', font=("Helvetica", 10), fill="red")

conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="Jyoti@123",
    database="identification"
)
cursor = conn.cursor()
cursor.execute("SELECT radius, power_value FROM matched_result")  # Adjust the query according to your table structure
results = cursor.fetchall()
conn.close()

point_positions = []
original_colors=[]

def change_label_background(label):
    label.configure(bg="light gray")
table_heading_label = tk.Label(input_frame, text="Indication Table", anchor="center",font=("times new roman",10,"bold"), height=2, width=26)
table_heading_label.pack(fill="x") 
 
    
previous_label = None

def label_click(event, i, label):
    global previous_label

    if previous_label is not None:
        previous_label.configure(bg="white") 

    change_label_background(label)  
    locate_and_change_circle(i)

    previous_label = label
    
    
def locate_points():
    canvas.delete("points")  
    y = center_y  
    frame_x_start = 10 
    frame_x_end = frame_width - 10 
    
    for i, (radius, power_value) in enumerate(results, start=1):
        if radius <= max_radius:
            x = center_x + radius 
            x = min(max(x, frame_x_start), frame_x_end)
            
            oval = canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill='yellow')
            text = canvas.create_text(x, y - 15)
            points.append((oval, text))
            original_colors.append(("yellow", "blue"))

            label = tk.Label(input_frame, text=f"  {i}.  Radius={radius}   Power={power_value}", bg="white", anchor="w",borderwidth=1,relief="solid",height=2, width=25)
            label.pack(fill="x")
            label.bind("<Button-1>", lambda event,  i=i-1, label=label: label_click(event, i, label))
            
selected_row=None

def locate_and_change_circle(index):
    global selected_row
    radius, power_value = results[index]
    angle = (index + 1) * (360 / num_circles)  
    x = center_x + radius  * math.cos(math.radians(angle))
    y = center_y - radius * math.sin(math.radians(angle))

    if selected_row is not None and selected_row != index:
        canvas.itemconfig(points[selected_row][0], fill=original_colors[selected_row][0])  # Revert oval color
        canvas.itemconfig(points[selected_row][1], fill=original_colors[selected_row][1])  # Revert text color

    canvas.itemconfig(points[index][0], fill="blue")  
    canvas.itemconfig(points[index][1], fill="blue") 

    selected_row = index

redraw_circles()
locate_points()

root.mainloop()
