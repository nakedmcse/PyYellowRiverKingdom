# Imports
import gameobjects
import shared
import validations
import random
import tkinter as tk
from tkinter import font, messagebox, Label, PhotoImage, Text

# Compute Turn Procedure
def computeTurn():
    startSeasonButton.config(state="disabled")
    shared.fieldWorkersvalue.config(state="disabled")
    shared.dykeWorkersvalue.config(state="disabled")
    shared.militiavalue.config(state="disabled")
    shared.growingvalue.config(state="disabled")
    fw = shared.fieldWorkersvalue.get()
    dw = shared.dykeWorkersvalue.get()
    mi = shared.militiavalue.get()
    pl = shared.growingvalue.get()
    messagebox.showwarning("Compute Turn Called","Compute Turn called with:\n\n"
                           + f"{fw} field workers\n"
                           + f"{dw} dyke workers\n"
                           + f"{mi} militia\n"
                           + f"{pl} planted")

# Show Splash Window
def showSplashWindow():
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
    splash_start_button = tk.Button(splashWindow, text="Start", font=button_font, command=lambda: splashStart(splashWindow))
    splash_start_button.place(x = 100, y = 900)
    splash_exit_button = tk.Button(splashWindow, text="Exit", font=button_font, command=splashWindow.quit)
    splash_exit_button.place(x=850,y=900)
    splashWindow.mainloop()

# Splash Window Start Game Button
def splashStart(splash):
    global startGame
    startGame = True
    splash.destroy()

# Show Instructions
def showInstructions():
    messagebox.showinfo("Instructions", "The kingdom is three villages. It is between the Yellow River and the mountains.\n\n"
        + "You have been chosen to take all the important decisions. Your poor predecessor was executed by thieves who live in the nearby mountains.\n\n"
        + "These thieves live off the villagers and often attack. The rice stored in the villages must be protected at all times.")
    messagebox.showinfo("Instructions","The year consists of three long seasons, Winter, Growing and Harvest. Rice is planted every Growing Season. You must decide how much is planted.\n\n"
        + "The river is likely to flood the fields and the villages. The high dyke between the river and the fields must be kept up to prevent a serious flood.\n\n"
        + "The people live off the rice that they have grown. It is a very poor living. You must decide what the people will work at each season so that they prosper under your leadership.")

# Game variables
shared.turns = []
startGame = False

# Program Start Point
showSplashWindow()

if startGame:
    showInstructions()

    # Main Game
    window = tk.Tk()
    window.title("Yellow River Kingdom")
    window.geometry("1024x800")

    # Create first turn
    shared.turns.append(gameobjects.GameState(f=5000 + random.randint(0,2000),g=0,p=300 + random.randint(0,100),
                                       fw=0,dw=0,m=0,s="winter",j=0,fd=None,ad=None))
    
    game_font = font.Font(size=16)
    # Render Map - TODO
    # Render HUD
    hud_frame = tk.LabelFrame(window, text = "Statistics", padx=5,pady=5)
    hud_frame.pack(padx=5, pady=5, fill="x", side="bottom")

    seasonlabel = tk.Label(hud_frame,text="Season:",font=game_font)
    seasonlabel.grid(row=0,column=0,sticky="w",padx=5)
    seasonvalue = tk.Label(hud_frame,text=shared.turns[-1].Season.capitalize(),font=game_font)
    seasonvalue.grid(row=0,column=1,sticky="w",padx=5)

    yearlabel = tk.Label(hud_frame,text="Year:",font=game_font)
    yearlabel.grid(row=0,column=2,sticky="w",padx=5)
    yearvalue = tk.Label(hud_frame,text=shared.turns[-1].year(),font=game_font)
    yearvalue.grid(row=0,column=3,sticky="w",padx=5)

    populationlabel = tk.Label(hud_frame,text="Population:",font=game_font)
    populationlabel.grid(row=1,column=0,sticky="w",padx=5)
    populationvalue = tk.Label(hud_frame,text=shared.turns[-1].Population,font=game_font)
    populationvalue.grid(row=1,column=1,sticky="w",padx=5)

    foodlabel = tk.Label(hud_frame,text="Food:",font=game_font)
    foodlabel.grid(row=1, column=2, sticky="w", padx=5)
    foodvalue = tk.Label(hud_frame,text=shared.turns[-1].Food,font=game_font)
    foodvalue.grid(row=1, column=3, sticky="w", padx=5)
    
    growinglabel = tk.Label(hud_frame,text="Planted:",font=game_font)
    growinglabel.grid(row=1, column=4, sticky="w", padx=5)
    shared.growingvalue = tk.Entry(hud_frame, validate='focusout', validatecommand=validations.validate_planted)
    shared.growingvalue.insert(0,shared.turns[-1].PlantedFood)
    shared.growingvalue.grid(row=1, column=5, sticky="w", padx=5)
    shared.growingvalue.bind("<KeyPress>", validations.validate_numeric)
    if(shared.turns[-1].Season == "winter"):
        shared.growingvalue.config(state="disabled")
    else:
        shared.growingvalue.config(state="normal")

    fieldWorkerslabel = tk.Label(hud_frame,text="Field Workers:",font=game_font)
    fieldWorkerslabel.grid(row=2, column=0, sticky="w", padx=5)
    shared.fieldWorkersvalue = tk.Entry(hud_frame, validate='focusout', validatecommand=validations.validate_population)
    shared.fieldWorkersvalue.insert(0,shared.turns[-1].FieldWorkers)
    shared.fieldWorkersvalue.grid(row=2, column=1, sticky="w", padx=5)
    shared.fieldWorkersvalue.bind("<KeyPress>", validations.validate_numeric)

    dykeWorkerslabel = tk.Label(hud_frame,text="Dyke Workers:",font=game_font)
    dykeWorkerslabel.grid(row=2, column=2, sticky="w", padx=5)
    shared.dykeWorkersvalue = tk.Entry(hud_frame, validate='focusout', validatecommand=validations.validate_population)
    shared.dykeWorkersvalue.insert(0,shared.turns[-1].DykeWorkers)
    shared.dykeWorkersvalue.grid(row=2, column=3, sticky="w", padx=5)
    shared.dykeWorkersvalue.bind("<KeyPress>", validations.validate_numeric)

    militialabel = tk.Label(hud_frame,text="Militia:",font=game_font)
    militialabel.grid(row=2, column=4, sticky="w", padx=5)
    shared.militiavalue = tk.Entry(hud_frame, validate='focusout', validatecommand=validations.validate_population)
    shared.militiavalue.insert(0,shared.turns[-1].Militia)
    shared.militiavalue.grid(row=2, column=5, sticky="w", padx=5)
    shared.militiavalue.bind("<KeyPress>", validations.validate_numeric)

    startSeasonButton = tk.Button(hud_frame, text="Start Season", command = computeTurn, font=game_font)
    startSeasonButton.grid(row=3, column=2, columnspan=2)

    hud_frame.grid_columnconfigure(0,weight=1)
    hud_frame.grid_columnconfigure(1,weight=1)
    hud_frame.grid_columnconfigure(2,weight=1)
    hud_frame.grid_columnconfigure(3,weight=1)
    hud_frame.grid_columnconfigure(4,weight=1)
    hud_frame.grid_columnconfigure(5,weight=1)

    window.mainloop()