# Imports
import gameobjects
import shared
import validations
import random
import tkinter as tk
from tkinter import font, messagebox, Label, PhotoImage, Text

# Compute Turn Procedure
def computeTurn():
    # Get values
    fw = int(shared.fieldWorkersvalue.get())
    dw = int(shared.dykeWorkersvalue.get())
    mi = int(shared.militiavalue.get())
    pl = int(shared.growingvalue.get())

    # Validate Population
    if validations.validate_submitted_population(fw,dw,mi) == False:
        messagebox.showerror("Population Mismatch",f"Your selections ({fw + dw + mi}) exceed your population - please try again")
        return

    # Fill in turn values
    shared.turns[-1].FieldWorkers = fw
    shared.turns[-1].DykeWorkers = dw
    shared.turns[-1].Militia = mi
    shared.turns[-1].PlantedFood = pl
    shared.turns[-1].Food = shared.turns[-1].Food - pl

    # Disable UI whilst computing
    startSeasonButton.config(state="disabled")
    shared.fieldWorkersvalue.config(state="disabled")
    shared.dykeWorkersvalue.config(state="disabled")
    shared.militiavalue.config(state="disabled")
    shared.growingvalue.config(state="disabled")
    
    # Attacks, Floods
    villagesHit = random.randint(0,3)
    if random.randint(0,2) == 1:
        # Flood
        shared.turns[-1].FloodDamage = gameobjects.FloodDamage(shared.turns[-1].Season,villagesHit,0,0,0,0,0,0)
        shared.turns[-1].FloodDamage.Calculate(dw,fw,mi,shared.turns[-1].Food,shared.turns[-1].Season)
        # TODO - Animate Flooding
        # Attack
        shared.turns[-1].AttackDamage = gameobjects.AttackDamage(shared.turns[-1].Season,0,0)
        shared.turns[-1].AttackDamage.Calculate(shared.turns[-1].Season,villagesHit,mi,shared.turns[-1].Food)
        # TODO - Animate Attack
    else:
        # Attack
        shared.turns[-1].AttackDamage = gameobjects.AttackDamage(shared.turns[-1].Season,0,0)
        shared.turns[-1].AttackDamage.Calculate(shared.turns[-1].Season,villagesHit,mi,shared.turns[-1].Food)
        # TODO - Animate Attack
        # Flood
        shared.turns[-1].FloodDamage = gameobjects.FloodDamage(shared.turns[-1].Season,villagesHit,0,0,0,0,0,0)
        shared.turns[-1].FloodDamage.Calculate(dw,fw,mi,shared.turns[-1].Food,shared.turns[-1].Season)
        # TODO - Animate Flooding
    
    #Starvation, Food growing, Population growth
    shared.turns[-1].Calculate()

    #Show turn report
    showReport(villagesHit)
    
    # Check for losing game
    if shared.turns[-1].checkEndGame():
        if shared.turns[-1].Food <= 0:
            failStarvation()
            window.quit()
        else:
            failPopulation()
            window.quit()

    # Check for ritual call
    if shared.turns[-1].ElapsedSeasons % 12 == 0 and shared.turns[-1].ElapsedSeasons > 0:
        showRitual()

    # Create next turn
    nextPlanted = shared.turns[-1].PlantedFood
    if shared.turns[-1].Season == "harvest":
        nextPlanted = 0
    shared.turns.append(gameobjects.GameState(f=shared.turns[-1].Food,g=nextPlanted,p=shared.turns[-1].Population,
                                       fw=0,dw=0,m=0,s=shared.turns[-1].nextSeason(),j=shared.turns[-1].ElapsedSeasons + 1,fd=None,ad=None))
    
    # Update HUD fields
    seasonvalue.config(text=shared.turns[-1].Season.capitalize())
    yearvalue.config(text=shared.turns[-1].year())
    populationvalue.config(text=shared.turns[-1].Population)
    foodvalue.config(text=shared.turns[-1].Food)
    shared.growingvalue.destroy()
    shared.growingvalue = tk.Entry(hud_frame, validate='focusout', validatecommand=validations.validate_planted)
    shared.growingvalue.insert(0,shared.turns[-1].PlantedFood)
    shared.growingvalue.grid(row=1, column=5, sticky="w", padx=5)
    shared.growingvalue.bind("<KeyPress>", validations.validate_numeric)
    shared.fieldWorkersvalue.destroy()
    shared.fieldWorkersvalue = tk.Entry(hud_frame, validate='focusout', validatecommand=validations.validate_population)
    shared.fieldWorkersvalue.insert(0,shared.turns[-1].FieldWorkers)
    shared.fieldWorkersvalue.grid(row=2, column=1, sticky="w", padx=5)
    shared.fieldWorkersvalue.bind("<KeyPress>", validations.validate_numeric)
    shared.dykeWorkersvalue.destroy()
    shared.dykeWorkersvalue = tk.Entry(hud_frame, validate='focusout', validatecommand=validations.validate_population)
    shared.dykeWorkersvalue.insert(0,shared.turns[-1].DykeWorkers)
    shared.dykeWorkersvalue.grid(row=2, column=3, sticky="w", padx=5)
    shared.dykeWorkersvalue.bind("<KeyPress>", validations.validate_numeric)
    shared.militiavalue.destroy()
    shared.militiavalue = tk.Entry(hud_frame, validate='focusout', validatecommand=validations.validate_population)
    shared.militiavalue.insert(0,shared.turns[-1].Militia)
    shared.militiavalue.grid(row=2, column=5, sticky="w", padx=5)
    shared.militiavalue.bind("<KeyPress>", validations.validate_numeric)
    window.update()

    # Re-enable HUD controls
    startSeasonButton.config(state="normal")
    shared.fieldWorkersvalue.config(state="normal")
    shared.dykeWorkersvalue.config(state="normal")
    shared.militiavalue.config(state="normal")
    if(shared.turns[-1].Season != "growing"):
        shared.growingvalue.config(state="disabled")
    else:
        shared.growingvalue.config(state="normal")

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

# Show failed starvation message
def failStarvation():
    messagebox.showerror("STARVATION","There was no food left. All of the people have run off and joined up "
                         + f"with the thieves after {shared.turns[-1].ElapsedSeasons} seasons of your misrule.")
    
# Show failed starvation message
def failPopulation():
    yearsmsg = f"{shared.turns[-1].year()} year"
    if shared.turns[-1].year() > 1:
        yearsmsg = yearsmsg + "s"
    messagebox.showerror("POPULATION GONE","There is no-one left! They have all been killed off by your decisions "
                         + f"after only {yearsmsg} of your misrule.")

# Show ritual (ability to quit every 12 seasons)
def showRitual():
    result = messagebox.askyesno("Village Ritual",f"We have survived for {shared.turns[-1].year()} years under your glorious control. "
                        + "By an ancient custom we must offer you the chance to lay down this terrible burden "
                        + "resume a normal life.\n\nAre you prepared to accept the burden of decision again?")
    if result == False:
        window.quit()  

# Show end of season report
def showReport(villages):
    populationLoss = shared.turns[-1].Population / shared.turns[-1].StartingPopulation
    foodLoss = shared.turns[-1].Food / (shared.turns[-1].Population + 1)
    
    populationMsg = ""
    if populationLoss < 0.5:
        populationMsg = "DISASTEROUS LOSSES!"
    elif populationLoss < 0.8:
        populationMsg = "WORRYING LOSSES!"
    elif populationLoss < 0.9:
        populationMsg = "You got off lightly"
    else:
        populationMsg = "Nothing to worry about"

    foodMsg = ""
    if foodLoss < 0.5:
        foodMsg = "STARVATION IMMINENT!"
    elif foodLoss < 0.75:
        foodMsg = "FOOD SUPPLY IS LOW!"
    else:
        foodMsg = "Nothing to worry about"

    messagebox.showwarning("Village Leader's Report",f"In the {shared.turns[-1].Season} Season of year {shared.turns[-1].year()} of your reign, the kingdom has suffered these losses:\n\n"
                           + f"{populationMsg}\n\n"
                           + "FLOOD DAMAGE\n"
                           + f"{villages} Villages Hit by Flooding\n"
                           + f"{shared.turns[-1].FloodDamage.FloodSize} Flood Size\n"
                           + f"{int(shared.turns[-1].FloodDamage.DykeWorkersKilled)} Dyke Workers Killed\n"
                           + f"{int(shared.turns[-1].FloodDamage.FieldWorkersKilled)} Field Workers Killed\n"
                           + f"{int(shared.turns[-1].FloodDamage.MilitiaKilled)} Militia Killed\n"
                           + f"{shared.turns[-1].FloodDamage.FoodLost} Food Lost\n"
                           + f"{shared.turns[-1].FloodDamage.PlantedFoodMultiplier} Planted Food Multiplier\n\n"
                           + "ATTACK DAMAGE\n"
                           + f"{shared.turns[-1].AttackDamage.MilitiaKilled} Militia Killed\n"
                           + f"{shared.turns[-1].AttackDamage.FoodLost} Food Lost\n\n"
                           + "CROPS/POPULATION\n"
                           + f"\n{foodMsg}\n\n"
                           + f"{shared.turns[-1].Population - shared.turns[-1].StartingPopulation} Population Change\n"
                           + f"{shared.turns[-1].Food - shared.turns[-1].StartingFood} Food Change")
    
# Show HUD
def showHUD():
    global window
    global startSeasonButton
    global seasonvalue
    global yearvalue
    global populationvalue
    global foodvalue
    global hud_frame
    
    game_font = font.Font(size=16)
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
    if(shared.turns[-1].Season != "growing"):
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

# Show Map
def showMap():
    global window,map_frame,river_image,village_image,scaled_village,mountain_image,scaled_mountain
    game_font = font.Font(size=16)
    map_frame = tk.LabelFrame(window, padx=0, pady=0, border=0, width=800, height=620, background="#6d9f56")
    map_frame.pack(padx=5, pady=5, fill="x", side="bottom")
    # River
    river_image = PhotoImage(file="Assets/river.png")
    river = tk.Label(map_frame, image=river_image, border=0)
    river.place(x = 0, y = 0)
    # Villages
    village_image = PhotoImage(file="Assets/village.png")
    width_scale = village_image.width() // 64
    height_scale = village_image.height() // 64
    scaled_village = village_image.subsample(width_scale,height_scale)
    village1 = tk.Label(map_frame, image=scaled_village, border=0)
    village1.place(x=350,y=150)
    village2 = tk.Label(map_frame, image=scaled_village, border=0)
    village2.place(x=500,y=300)
    village3 = tk.Label(map_frame, image=scaled_village, border=0)
    village3.place(x=500,y=450)
    # Mountains
    mountain_image = PhotoImage(file="Assets/mountain.png")
    scaled_mountain = mountain_image.subsample(2,2)
    mountain1 = tk.Label(map_frame, image=mountain_image, border=0)
    mountain1.place(x=650,y=0)
    mountain1a = tk.Label(map_frame, image=scaled_mountain, border=0)
    mountain1a.place(x=850,y=10)
    mountain1b = tk.Label(map_frame, image=scaled_mountain, border=0)
    mountain1b.place(x=920,y=80)
    mountain1c = tk.Label(map_frame, image=scaled_mountain, border=0)
    mountain1c.place(x=800,y=100)
    mountain1d = tk.Label(map_frame, image=scaled_mountain, border=0)
    mountain1d.place(x=870,y=150)
    mountain2 = tk.Label(map_frame, image=mountain_image, border=0)
    mountain2.place(x=750,y=200)
    mountain2a = tk.Label(map_frame, image=scaled_mountain, border=0)
    mountain2a.place(x=920,y=220)
    mountain2b = tk.Label(map_frame, image=scaled_mountain, border=0)
    mountain2b.place(x=810,y=300)
    mountain3 = tk.Label(map_frame, image=mountain_image, border=0)
    mountain3.place(x=800,y=375)
    mountain3a = tk.Label(map_frame, image=scaled_mountain, border=0)
    mountain3a.place(x=920,y=350)
    mountain3b = tk.Label(map_frame, image=scaled_mountain, border=0)
    mountain3b.place(x=840,y=500)
    mountain3c = tk.Label(map_frame, image=scaled_mountain, border=0)
    mountain3c.place(x=910,y=472)
    mountain3d = tk.Label(map_frame, image=scaled_mountain, border=0)
    mountain3d.place(x=920,y=550)
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
        
    # Render HUD
    showHUD()

    # Render Map
    showMap()

    window.mainloop()