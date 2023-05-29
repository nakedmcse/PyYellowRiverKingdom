# PyYellowRiverKingdomGameObjects
import random

# Game state
class GameState:
    def __init__(self,f,g,p,fw,dw,m,s,j,fd,ad):
        self.Food = f
        self.StartingFood = f
        self.PlantedFood = g
        self.Population = p
        self.StartingPopulation = p
        self.FieldWorkers = fw
        self.DykeWorkers = dw
        self.Militia = m
        self.Season = s
        self.ElapsedSeasons = j
        self.FloodDamage = fd
        self.AttackDamage = ad

    def checkEndGame(self):
        return ((self.Food <= 0) or (self.Population <= 0))
    
    def addThieves(self):
        self.Population = self.Population + 50 + random.randint(0,100)
        return
    
    def year(self):
        return(int(self.ElapsedSeasons / 3) + 1)
    
    def nextSeason(self):
        cases = {
            "winter": "growing",
            "growing": "harvest",
            "harvest": "winter"
        }
        return cases.get(self.Season,"unknown")
    
    def Calculate(self):
        if self.FieldWorkers == 0:
            self.PlantedFood = 0
        if self.PlantedFood > 1000:
            self.PlantedFood = 1000
        elif self.PlantedFood < 0:
            self.PlantedFood = 0
        
        # Calculate Growth by Season
        if self.Season == "growing":
            self.PlantedFood = int(round(self.PlantedFood * ((self.FieldWorkers - 10)/self.FieldWorkers)))
            self.PlantedFood = int(self.PlantedFood * self.FloodDamage.PlantedFoodMultiplier)
        elif self.Season == "harvest":
            self.PlantedFood = int(round(18 * (11 + random.randint(0,3)) * (0.05 - 1/self.FieldWorkers) * self.PlantedFood))
            self.PlantedFood = int(self.PlantedFood * self.FloodDamage.PlantedFoodMultiplier)
            # Increase Food
            self.Food = self.Food + self.PlantedFood
        
        # Consume Food based on population
        if self.Population <= 0:
            return
        FoodRatio = self.Food/self.Population
        StarvationDeaths = 0
        if FoodRatio > 5:
            FoodRatio = 4
        elif FoodRatio < 2:
            #Starvation
            self.Population = 0
            return
        elif FoodRatio > 4:
            FoodRatio = 3.5
        else:
            StarvationDeaths = int(round(self.Population * (7 - FoodRatio)/7))
            FoodRatio = 3
            self.Population = self.Population - StarvationDeaths
            if self.Population < 0:
                self.Population = 0

        self.Food = int(round(self.Food - self.Population * FoodRatio - StarvationDeaths * (FoodRatio / 2)))
        if self.Food < 0:
            self.Food = 0

        # Handle population decrease
        self.Population = self.Population - int(self.FloodDamage.DykeWorkersKilled) - int(self.FloodDamage.FieldWorkersKilled) - int(self.FloodDamage.MilitiaKilled)
        self.Population = self.Population - int(self.AttackDamage.MilitiaKilled)

        # Handle population increase
        if self.Population < 200 and random.randint(0,3) == 1:
            self.addThieves()
        self.Population = int(round(self.Population * 1.045))
        return
    
# Flood damage
class FloodDamage: 
    def __init__(self,s,v,dw,fw,m,ff,fd,g):
        self.FloodSize = s
        self.VillagesHit = v
        self.DykeWorkersKilled = dw
        self.FieldWorkersKilled = fw
        self.MilitiaKilled = m
        self.FoodLost = ff
        self.PopulationLost = fd
        self.PlantedFoodMultiplier = g

    def SetSize(self,dw,s):
        #Size of flood by Season
        if s == "growing":
            self.FloodSize = (random.randint(0,330)/(dw + 1))
        elif s == "harvest":
            self.FloodSize = ((random.randint(0,100) + 60)/(dw + 1))
        else:
            self.FloodSize = 0
            self.VillagesHit = 0
            self.DykeWorkersKilled = 0
            self.FieldWorkersKilled = 0
            self.MilitiaKilled = 0
            self.FoodLost = 0
            self.PlantedFoodMultiplier = 1
            self.PopulationLost = 0 

    def Calculate(self,dw,fw,m,f,s,v):
        #No Flood then return
        if self.FloodSize == 0:
            return
        self.VillagesHit = v
        #Population Damage
        self.DykeWorkersKilled = (dw // 10)*(10 - self.FloodSize)
        self.FieldWorkersKilled = (fw // 10)*(10 - self.FloodSize)
        self.MilitiaKilled = (m // 6)*(6 - self.VillagesHit)
        self.PopulationLost = self.DykeWorkersKilled + self.FieldWorkersKilled + self.MilitiaKilled

        #Food Damage
        self.FoodLost = f * (self.VillagesHit // 6)
        if s == "growing":
            self.PlantedFoodMultiplier = (20 - self.FloodSize) / 20
        elif s == "harvest":
            self.PlantedFoodMultiplier = (10 - self.FloodSize) / 10
        else:
            self.PlantedFoodMultiplier = 1
        return

# Attack Damage
class AttackDamage:
    def __init__(self,s,mk,fl):
        self.MilitiaKilled = mk
        self.FoodLost = fl

    def Calculate(self,s,vf,m,f):
        # All villages flooded return
        if vf == 3:
            return
        
        # Based on season decide if attacked
        diceRoll = random.randint(0,100)
        if s == "winter" and diceRoll < 50:
            return
        elif s == "growing" and diceRoll < 20:
            return
        elif s == "harvest" and diceRoll < 60:
            return
        
        # Calculate damage based on season
        baseDamage = 0
        if s == "winter":
            baseDamage = 200 + random.randint(0,70) - m
        elif s == "growing":
            baseDamage = 30 + random.randint(0,200) - m
        elif s == "harvest":
            baseDamage = random.randint(0,400) - m
        
        # Militia Killed
        self.MilitiaKilled = int(round((m * (baseDamage/400))))
        # Food Lost
        self.FoodLost = int(round((baseDamage * (f/729) + random.randint(0,2000-m)/10)))
        if self.FoodLost < 0:
            self.FoodLost = 0
        elif self.FoodLost > 2000:
            self.FoodLost = 1900 + random.randint(0,200)
        return