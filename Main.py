#https://pypi.org/project/PyDirectInput/
#https://pypi.org/project/mousekey/

# ↑ Note ↑

from PIL import Image,ImageTk,ImageDraw
import tkinter as tk
from mss import mss
import customtkinter as ctk
from mousekey import MouseKey
import pywinstyles
import webbrowser
import requests
import win32api,win32con
from time import sleep
import cv2
import numpy as np
import keyboard

mkey=MouseKey()
stc=mss()

#------------------------------------------------------------
# Values
#------------------------------------------------------------

# Get the screen resolution
try:
	screens_resolution=mkey.get_screen_resolution()
except:
	screens_resolution=[1920,1080]
x_screens_resolution=screens_resolution[0];y_screens_resolution=screens_resolution[1]
mon={"top": 0,"left": int(x_screens_resolution/4.8),"width": int(x_screens_resolution/1.92),"height": int(y_screens_resolution/3)}

speed="Normal"						# Default speed
Resize=0.37							# Resize the screenshot

map_img = np.array(stc.grab(mon))	# Grab a screenshot of the monitor
detected_images = []  				# Store the names of detected images
max_val = 0  						# Initialize max_val to keep track of the highest match percentage
max_img = None  					# Initialize max_img to keep track of the image with the highest match percentage
matches = []  						# Store the matches
w = 0  								# Initialize the width of the template image
h = 0  								# Initialize the height of the template image

# The coordinates of the buttons
def Left_Or_Right_data_of_coordinates():
	global restock_x,restock_y,Add_Doughx,Add_Doughy,Add_Sauce_x,Add_Sauce_y,Add_cheese_x,Add_cheese_y,Add_pepperoni_x,Add_pepperoni_y,Add_ham_x,Add_ham_y,Add_veg_x,Add_veg_y,default_x,default_y,done_x,done_y,Left_Or_Right_data_of_coordinates_BOX,image_paths

	if Left_Or_Right_data_of_coordinates_BOX.get()==True:
		Left_Or_Right_data_of_coordinates_BOX.configure(text="Left Side",font=("Arial",int(14),"bold"))					# Change the text of the button

		# Image paths
		image_paths = ["Pizza\\restock_Left.png","Pizza\\ham_Left.png","Pizza\\vea_Left.png","Pizza\\fgy_Left.png","Pizza\\cheese_Left.png"]

		restock_x,restock_y=				int(x_screens_resolution/float(2.73)),int(y_screens_resolution/1.015)		# Restock button
		Add_Doughx,Add_Doughy=				int(x_screens_resolution/float(1.95)),int(y_screens_resolution/4.9)			# Dough button
		Add_Sauce_x,Add_Sauce_y=0,			int(y_screens_resolution/float(16.3))										# Sauce button
		Add_cheese_x,Add_cheese_y=0,		int(y_screens_resolution/float(16.3))										# Cheese button
		Add_pepperoni_x,Add_pepperoni_y=0,	int(y_screens_resolution/float(16.3))										# Pepperoni button
		Add_ham_x,Add_ham_y=				int(x_screens_resolution/float(16)),0										# Ham button
		Add_veg_x,Add_veg_y=				int(-x_screens_resolution/float(13.3)),0									# Veg button
		done_x,done_y=						int(x_screens_resolution/float(1.5)),int(y_screens_resolution/6.58)			# Done button
		default_x,default_y=				int(x_screens_resolution/float(1.64)),int(y_screens_resolution/9)			# Default button

	else:
		Left_Or_Right_data_of_coordinates_BOX.configure(text="Right Side",font=("Arial",int(14),"bold"))				# Change the text of the button

		# Image paths
		image_paths = ["Pizza\\restock_Right.png","Pizza\\ham_Right.png","Pizza\\vea_Right.png","Pizza\\fgy_Right.png","Pizza\\cheese_Right.png"]

		restock_x,restock_y=				int(x_screens_resolution/float(1.75)),int(y_screens_resolution/1.07)		# Restock button
		Add_Doughx,Add_Doughy=				int(x_screens_resolution/float(2.95)),int(y_screens_resolution/4.32)		# Dough button
		Add_Sauce_x,Add_Sauce_y=0,			int(y_screens_resolution/float(16.3))										# Sauce button
		Add_cheese_x,Add_cheese_y=0,		int(y_screens_resolution/float(16.3))										# Cheese button
		Add_pepperoni_x,Add_pepperoni_y=0,	int(y_screens_resolution/float(16.3))										# Pepperoni button
		Add_ham_x,Add_ham_y=				int(x_screens_resolution/float(16)),0										# Ham button
		Add_veg_x,Add_veg_y=				int(-x_screens_resolution/float(13.3)),0									# Veg button
		done_x,done_y=						int(x_screens_resolution/float(2)),int(y_screens_resolution/5.6)			# Done button
		default_x,default_y=				int(x_screens_resolution/float(2.22)),int(y_screens_resolution/3.85)		# Default button

#------------------------------------------------------------
# Functions
#------------------------------------------------------------

def take_screenshot():
	img=stc.grab(mon) 														# Grab a screenshot of the monitor
	img_pil=Image.frombytes("RGB",img.size,img.bgra,"raw","BGRX")			# Convert the screenshot to a PIL image

	# Coordinates data points
	Coordinates_data=[(Add_Doughx,Add_Doughy),(done_x,done_y)]

	# Draw the Coordinates data on the screenshot
	draw=ImageDraw.Draw(img_pil);dot_radius=int(x_screens_resolution/192);outline_radius=int(x_screens_resolution/384)

	for point in Coordinates_data:
		x,y=point																								# Get the coordinates of the point

		scale_factor_x=img.width / mon["width"];scale_factor_y=img.height / mon["height"]						# Calculate the scale factor
		adjusted_x=int((x - mon["left"]) * scale_factor_x);adjusted_y=int((y - mon["top"]) * scale_factor_y)	# Calculate adjusted coordinates

		# Calculate the bounding boxes for the dot and outline
		dot_box=[(adjusted_x - dot_radius,adjusted_y - dot_radius),(adjusted_x + dot_radius,adjusted_y + dot_radius)];outline_box=[(adjusted_x - outline_radius,adjusted_y - outline_radius),(adjusted_x + outline_radius,adjusted_y + outline_radius)]

		draw.ellipse(outline_box,outline="red",width=5);draw.ellipse(dot_box,fill="red")

	img_pil=img_pil.resize((int(mon["width"] * Resize),int(mon["height"] * Resize)))			# Resize the image to fit the screen
	img_tk=ImageTk.PhotoImage(img_pil)															# Convert the PIL image to a Tkinter image

	# Update the label with the new image
	label.config(image=img_tk)				# Update the label with the new image
	label.image=img_tk 						# Keep a reference to the image
	app.after(33,take_screenshot)			# Schedule the next update

def on_click_Github_button():
	webbrowser.open("https://github.com/DisguisedOwI/Pizza-Bakery-Fram-Bot")

def check_for_updates():
	try:
		# Get the latest release from the GitHub API
		release_url="https://api.github.com/repos/DisguisedOwI/Pizza-Bakery-Fram-Bot/releases/latest"
		release_data=requests.get(release_url).json()	# Get the release data
		latest_version=release_data["tag_name"]			# Get the latest version number
		latest_version=latest_version[1:]  				# Remove the "v" from the version number
		return latest_version							# Return the latest version number

	except Exception as e:
		print(f"Error checking for updates: {e}")		# Print the error message
		return "0.0"									# Return 0.0 if an error occurs

def click(x,y):
	mkey.move_to_natural(x,y) 		# Move the mouse to the specified coordinates
	sleep(0.1);win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0);sleep(0.1);win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
	app.update()					# Update the application window

def FastClick(x,y):
	mkey.left_click_xy_natural(
		x,y,						# x and y coordinates
		delay=0,					# delay before clicking
		min_variation=-3,			# minimum variation of the mouse movement
		max_variation=3,			# maximum variation of the mouse movement
		use_every=4,				# use every nth coordinate
		#sleeptime=(0.005,0.009),	# sleep time between each coordinate
		print_coords=False,			# print the coordinates
		percent=200,				# percentage of the mouse movement
)
	sleep(0.009)					# Wait for 0.009 seconds

	app.update()					# Update the application window

#------------------------------------------------------------
# Bot functions
#------------------------------------------------------------

def	StarterBot():
	global map_img,detected_images,max_val,max_img,speed,matches,w,h
	print("Hold 'q' to Stop the Bot")
	print("and Start in 1 seconds")

	sleep(1)
	app.title("Pizza Bakery Fram Bot v6 - Running")														# Set the application title to "Running"

	image_names = ["ReStock","ham","veg","pepperoni","cheese"]											# Names of the images
	template_images = [cv2.imread(path,cv2.IMREAD_UNCHANGED) for path in image_paths]					# Load the template images

	speed=speed_button.get()																			# Get the speed to the bot

	while True:
		if keyboard.is_pressed("q"):app.title("Pizza Bakery Fram Bot v6");break							# Check if the "q" key is pressed

		map_img = np.array(stc.grab(mon))  # Grab a screenshot of the monitor

		highest_val = -1  # Initialize a variable to store the highest value
		highest_img_name = ""  # Variable to store the name of the image with the highest value

		for i, template_img in enumerate(template_images):  # Loop through the template images
			result = cv2.matchTemplate(map_img, template_img, cv2.TM_CCOEFF_NORMED)  # Match the template image to the screenshot
			_, match_val, _, max_loc = cv2.minMaxLoc(result)  # Get the match percentage and location of the highest match
			print(f"{image_names[i]}: {match_val}")  # Print the match percentage

			if match_val > highest_val:  # If the current match value is higher than the stored highest
				highest_val = match_val  # Update the highest value
				highest_img_name = image_names[i]  # Store the name of the image with the highest match

		# If the highest value is greater than the threshold, add the corresponding image to the detected_images list
		if highest_val > 0.65:  # Threshold set to 65%
			detected_images = [highest_img_name]  # Clear the list and add only the highest match
			print(f"Detected: {', '.join(detected_images)}")  # Print the names of the detected images
#------------------------------------------------------------
# Fast mode
#------------------------------------------------------------

			if speed == "Fast":																							# Check if the speed is set to "Fast"
				if "ReStock" in detected_images:																		# Check if the "ReStock" image was detected
					for a in range(2):																					# Click the "ReStock" button twice
						FastClick(restock_x,restock_y);sleep(0.2)														# Click the "ReStock" button and wait for 0.2 seconds
						if keyboard.is_pressed("q"):app.title("Pizza Bakery Fram Bot v6");break							# Check if the "q" key is pressed
					for a in range(2):																					# Click the "Dough" button twice
						FastClick(Add_Doughx,Add_Doughy);sleep(0.2)														# Click the "Dough" button and wait for 0.2 seconds
						if keyboard.is_pressed("q"):app.title("Pizza Bakery Fram Bot v6");break							# Check if the "q" key is pressed
					FastClick(default_x,default_y);sleep(1.8)															# Click the "Done" and "Default" buttons and wait for 1 second

				if "ham" or "veg" or "pepperoni" or "cheese" in detected_images:										# Check if any of the ingredient images were detected
					for a in range(2):FastClick(Add_Doughx,Add_Doughy)													# Click the "Dough" button twice
					FastClick(Add_Doughx+Add_Sauce_x,Add_Doughy+Add_Sauce_y)											# Click the "Sauce" button
					if keyboard.is_pressed("q"):app.title("Pizza Bakery Fram Bot v6");break								# Check if the "q" key is pressed
					FastClick(Add_Doughx+Add_cheese_x,Add_Doughy+Add_cheese_y)											# Click the "Cheese" button
					if keyboard.is_pressed("q"):app.title("Pizza Bakery Fram Bot v6");break								# Check if the "q" key is pressed
					if "ham" in detected_images:FastClick(Add_Doughx+Add_ham_x,Add_Doughy+Add_ham_y)					# Check if the "Ham" image was detected
					if "veg" in detected_images:FastClick(Add_Doughx+Add_veg_x,Add_Doughy+Add_veg_y)					# Check if the "Veg" image was detected
					if "pepperoni" in detected_images:FastClick(Add_Doughx+Add_pepperoni_x,Add_Doughy+Add_pepperoni_y)	# Check if the "Pepperoni" image was detected
					if keyboard.is_pressed("q"):app.title("Pizza Bakery Fram Bot v6");break								# Check if the "q" key is pressed
					FastClick(done_x,done_y);FastClick(default_x,default_y);sleep(1.8)									# Click the "Done" and "Default" buttons and wait for 1 second

#------------------------------------------------------------
# Slow mode
#------------------------------------------------------------

			elif speed == "Normal":																						# Check if the speed is set to "Normal"
				if "ReStock" in detected_images:																		# Check if the "ReStock" image was detected
					for a in range(2):																					# Click the "ReStock" button twice and wait for 0.2 seconds
						click(restock_x,restock_y);sleep(0.2)															# Click the "ReStock" button and wait for 0.2 seconds
						if keyboard.is_pressed("q"):app.title("Pizza Bakery Fram Bot v6");break							# Check if the "q" key is pressed
					for a in range(2):																					# Click the "Dough" button twice and wait for 0.2 seconds
						click(Add_Doughx,Add_Doughy);sleep(0.2)															# Click the "Dough" button twice and wait for 0.2 seconds
						if keyboard.is_pressed("q"):app.title("Pizza Bakery Fram Bot v6");break							# Check if the "q" key is pressed
					click(default_x,default_y);sleep(1.8)																# Click the "Done" and "Default" buttons and wait for 1 second

				if "ham" or "veg" or "pepperoni" or "cheese" in detected_images:										# Check if any of the ingredient images were detected
					for a in range(2):																					# Click the "Dough" button twice
						click(Add_Doughx,Add_Doughy)																	# Click the "Dough" button twice
						if keyboard.is_pressed("q"):app.title("Pizza Bakery Fram Bot v6");break							# Check if the "q" key is pressed
					click(Add_Doughx+Add_Sauce_x,Add_Doughy+Add_Sauce_y)												# Click the "Sauce" button
					if keyboard.is_pressed("q"):app.title("Pizza Bakery Fram Bot v6");break								# Check if the "q" key is pressed
					click(Add_Doughx+Add_cheese_x,Add_Doughy+Add_cheese_y)												# Click the "Cheese" button
					if keyboard.is_pressed("q"):app.title("Pizza Bakery Fram Bot v6");break								# Check if the "q" key is pressed
					if "ham" in detected_images:click(Add_Doughx+Add_ham_x,Add_Doughy+Add_ham_y)						# Check if the "Ham" image was detected
					if "veg" in detected_images:click(Add_Doughx+Add_veg_x,Add_Doughy+Add_veg_y)						# Check if the "Veg" image was detected
					if "pepperoni" in detected_images:click(Add_Doughx+Add_pepperoni_x,Add_Doughy+Add_pepperoni_y)		# Check if the "Pepperoni" image was detected
					if keyboard.is_pressed("q"):app.title("Pizza Bakery Fram Bot v6");break								# Check if the "q" key is pressed
				click(done_x,done_y);click(default_x,default_y);sleep(1.8)												# Click the "Done" and "Default" buttons and wait for 1 second

#------------------------------------------------------------
# The Ui of the application
#------------------------------------------------------------

# Ui appearance
ctk.set_appearance_mode("dark")			# Set the appearance mode
ctk.set_default_color_theme("blue")		# Set the default color theme

# Create the main application window using customtkinter
app=ctk.CTk()							# Create the application window
app.geometry("400x200")					# Set application window size
app.title("Pizza Bakery Fram Bot v6")	# Set application title
app.iconbitmap("Pizza\\icon.ico")		# Set application icon
app.resizable(False,False)				# Disable resizing
app.wm_attributes("-topmost",1)			# Always on top

label=tk.Label(app); label.pack()		# Create a label for the screenshot

# The Start button
Starter_Bot=ctk.CTkButton(app,text="Starter Bot",command=StarterBot,font=("Arial",int(16),"bold"));Starter_Bot.place(relx=0.5,rely=0.775,anchor=tk.CENTER)

#Left or Right side
Left_Or_Right_data_of_coordinates_BOX = ctk.CTkCheckBox(app,text="Right Side",variable=tk.BooleanVar(),font=("Arial",14,"bold"),command=Left_Or_Right_data_of_coordinates);Left_Or_Right_data_of_coordinates_BOX.place(x = 10,y = 144);Left_Or_Right_data_of_coordinates()

# The dropdown menu
speed_button=ctk.CTkOptionMenu(app,values=["Normal","Fast"],height=20,width=90,font=("Arial",int(14),"bold"));speed_button.place(x=10,y=174);speed_button.set("Normal")

# The Stop button
ctk.CTkLabel(app,text="Hold 'q' to Stop!",font=("Arial",16,"bold")).place(relx=0.5,rely=0.93,anchor=tk.CENTER)

# The GitHub button
Image_import_button_icon=Image.open("Pizza\\github.png");Image_import_button_icon=Image_import_button_icon.resize((20,20));Image_import_button_icon=ctk.CTkImage(Image_import_button_icon);Github_button=ctk.CTkButton(app,text="",command=on_click_Github_button,image=Image_import_button_icon,width=20,height=20);Github_button.place(relx=0.92,rely=0.775,anchor=tk.CENTER)

#------------------------------------------------------------
# Check for updates
#------------------------------------------------------------

# Check for updates and current version
latest_version=check_for_updates();current_version="6.0"

if latest_version!=current_version:
	print(f"Current version: {current_version}");print(f"Latest version: {latest_version}");print("An update is available!")

	Update_text=ctk.CTkButton(app,text="Update Available!",font=("Arial",12,"underline","italic"),command=on_click_Github_button,fg_color="#242424",hover_color="#242424",width=20,height=10);Update_text.place(relx=0.795,rely=0.92,anchor=tk.CENTER)

	update_available=Image.open("Pizza\\alert-circle.png");update_available=update_available.resize((20,20));update_available=ctk.CTkImage(update_available);update_available_Image=ctk.CTkLabel(app,image=update_available,text="",width=20,height=20);update_available_Image.place(relx=0.95,rely=0.925,anchor=tk.CENTER);pywinstyles.set_opacity(update_available_Image,color="#242424")

#------------------------------------------------------------
# Start the application
#------------------------------------------------------------

# Start updating the screenshot
take_screenshot()

# Start the tkinter main loop
app.mainloop()