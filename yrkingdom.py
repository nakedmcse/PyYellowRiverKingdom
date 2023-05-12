# Imports
import gameobjects
import random
import tkinter as tk
from tkinter import font, messagebox, Label, PhotoImage, Text

# Game variables
turns = []
startGame = False

# Splash Window Start Game
def splashStart():
    global startGame
    global splashWindow
    startGame = True
    splashWindow.destroy()

# Splash Window
splashWindow = tk.Tk()
splashWindow.title("Yellow River Kingdom")
splashWindow.geometry("1024x1000")

# Load background
background_image = PhotoImage(file="Assets/splashwindow.png")
bgnd = tk.Label(splashWindow, image=background_image, width=1024, height=1000)
bgnd.place(x=0,y=0)

# Title
label_font = font.Font(family="Arial", size=48, weight="bold")
label = tk.Label(splashWindow,text="Yellow River Kingdom", font=label_font, fg="red")
label.place(x=170,y=50)

# Start and Exit buttons
button_font = font.Font(size=24,weight="bold")
splash_start_button = tk.Button(splashWindow, text="Start", font=button_font, command=splashStart)
splash_start_button.place(x = 100, y = 900)
splash_exit_button = tk.Button(splashWindow, text="Exit", font=button_font, command=splashWindow.quit)
splash_exit_button.place(x=850,y=900)
splashWindow.mainloop()

if startGame:
    # Instructions
    messagebox.showinfo("Instructions", "The kingdom is three villages. It is between the Yellow River and the mountains.\n\n"
        + "You have been chosen to take all the important decisions. Your poor predecessor was executed by thieves who live in the nearby mountains.\n\n"
        + "These thieves live off the villagers and often attack. The rice stored in the villages must be protected at all times.")
    messagebox.showinfo("Instructions","The year consists of three long seasons, Winter, Growing and Harvest. Rice is planted every Growing Season. You must decide how much is planted.\n\n"
        + "The river is likely to flood the fields and the villages. The high dyke between the river and the fields must be kept up to prevent a serious flood.\n\n"
        + "The people live off the rice that they have grown. It is a very poor living. You must decide what the people will work at each season so that they prosper under your leadership.")

    # Main Game
    window = tk.Tk()
    window.title("Yellow River Kingdom")
    window.geometry("1024x1000")

    # Create first turn
    turns.append(gameobjects.GameState(f=5000 + random.randint(0,2000),g=0,p=300 + random.randint(0,100),
                                       fw=0,dw=0,m=0,s="winter",j=0,fd=None,ad=None))
    
    game_font = font.Font(size=18)
    foodlabel = tk.Label(window,text=f"Food:{turns[0].Food}",font=game_font)
    foodlabel.pack()
    populationlabel = tk.Label(window,text=f"Population:{turns[0].Population}",font=game_font)
    populationlabel.pack()
    seasonlabel = tk.Label(window,text=f"Season:{turns[0].Season}",font=game_font)
    seasonlabel.pack()

    window.mainloop()