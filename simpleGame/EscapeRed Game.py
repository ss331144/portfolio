'''
RedEscape Game

Description:
-------------
This is a simple Python game built using Tkinter, where the player controls a red circular character
on the screen. The goal is to navigate the character from the starting position to the green "king" 
circle while avoiding black enemy circles scattered randomly on the screen.

Gameplay:
-------------
- The player moves the red character using the arrow keys (up, down, left, right).
- Enemies are randomly generated black circles that periodically respawn.
- If the character collides with any enemy, the game ends with a "You Lose" screen.
- Reaching the green "king" circle triggers a win screen showing the time taken to complete the game.
- The game saves the best time record in a file and displays it.

Main Components:
-----------------
- Tkinter Canvas for rendering the game elements (character, enemies, goal).
- Keyboard input detection using the 'keyboard' module.
- Random enemy placement and respawning every few seconds.
- Collision detection between player and enemies or player and goal.
- Timer tracking total game duration.

Functions:
------------
- start(): Initializes the game elements, removes the welcome screen, and starts the movement loop.
- move(): Detects keyboard input and moves the character accordingly, checks collisions.
- createEnemy(): Creates enemy circles at random positions on the canvas.
- CheakEnemyOn(CoordsEnemys): Checks if the character overlaps with any enemy, triggers loss if so.
- LoseThrome(): Handles game loss by showing a message and disabling the character.
- winGame(): Checks if the character reached the goal and displays win message with elapsed time.
- gameRull(): Shows the game rules in a popup window.
- destroyGame(): Destroys the main game window.
- saveRecord(value): Saves the best game time record in a file and shows the previous record.

Usage:
---------
Run this script. On the welcome screen, click "Start game" to begin. Use arrow keys to move the red 
circle. Avoid black enemies and reach the green circle to win.

Dependencies:
--------------
- Python standard library modules: tkinter, random, datetime
- External modules: keyboard, pyautogui, screeninfo

Note:
-------
This game requires administrative privileges on some systems for the 'keyboard' module to detect key presses.

'''


#game
import keyboard
import tkinter
from tkinter import messagebox
import screeninfo
import random
import pyautogui
import datetime

def start():
    global canvas
    global character
    global characterLocation
    global Kgame
    global firstTime
    firstTime = datetime.datetime.now()
    characterSize = 20
    
    labelTitleGame.destroy()
    buttonStart.destroy()
    buttonrull.destroy()
    
    canvas = tkinter.Canvas(root, width=screen_width, height=screen_height)
    canvas.grid(row=2, column=2)
    character = canvas.create_oval(characterSize, characterSize, characterSize+10, characterSize+10, fill="red")
    canvas.move(character, 10, 0)
    characterLocation = canvas.coords(character)
    
    x=1810
    y=570
    kingWin =canvas.create_oval(x, y, x+90, y+90, fill="green")
    Kgame = canvas.coords(kingWin)
    createEnemy()
    winGame()
    root.after(100, move)

    
def move():
    global CoordsEnemys 
    global character
    global characterLocation
    if (keyboard.is_pressed('up')):
        canvas.move(character, 0, -10)
        characterLocation = canvas.coords(character)
        winGame()
        CheakEnemyOn(CoordsEnemys)
        
    if keyboard.is_pressed('down'):
        canvas.move(character, 0, 10)
        characterLocation = canvas.coords(character)

        winGame()
        CheakEnemyOn(CoordsEnemys)
        
    if keyboard.is_pressed('right'):
        canvas.move(character, 10, 0)
        characterLocation = canvas.coords(character)
        CheakEnemyOn(CoordsEnemys)
        winGame()
        
    if keyboard.is_pressed('left'):
        canvas.move(character, -10, 0)
        characterLocation = canvas.coords(character) # get the coords of character
        winGame()
        CheakEnemyOn(CoordsEnemys)                          # cheke if character touch in enemy

    root.after(5, move)

def createEnemy():
    global characterLocation
    global CoordsEnemys
    change=70
    for i in range(55):
        Enemy_x=random.randint(0  ,1850 )
        Enemy_y=random.randint(0  ,980 )
        
        Enemy = canvas.create_oval(Enemy_x, Enemy_y, Enemy_x+change, Enemy_y+change, fill="black")
        coords = canvas.coords (Enemy)
        if (characterLocation[0]>coords[0] and
                characterLocation[1]>coords[1] and
                characterLocation[2]<coords[2] and
                characterLocation[3]<coords[3]):
            continue
        else: CoordsEnemys.append(coords)
        
    root.after(2500, lambda: (createEnemy( ) ) )
def CheakEnemyOn(CoordsEnemys):
    global characterLocation
    a = characterLocation
    b = CoordsEnemys
    for coords in b :
        if (a[0]>coords[0] and
                a[1]>coords[1] and
                a[2]<coords[2] and
                a[3]<coords[3]
            ):
            LoseThrome()

def LoseThrome():
    global characterLocation
    global character
    #canvas.destroy()
    #root.destroy()
    canvas.coords( character ,  -200,-200,-200,-200)
    
    destroyGame()
    a = tkinter.Tk()
    a.geometry("800x600")
    a.title("Result")
    label=tkinter.Label(a,text="You Lose !" ,width=20,height=5 , bg="red",font=("Ariel",30,"bold"))
    label.grid(row=0, column=0)\

                      
    
    BottonExi = tkinter.Button(a,text="Exit" ,width=20 , height=10, command=lambda :  a.destroy() ,bg="green",font=("Ariel",12,"bold"))
    BottonExi.grid(row=1 , column=0)
    
    #destroyGame()
    
def winGame():
    global characterLocation
    global Kgame
    global firstTime
    
    a= characterLocation

    if (a[0]>Kgame[0] and
        a[1]>Kgame[1] and
        a[2]<Kgame[2] and
        a[3]<Kgame[3] 
        ) :
        aftertime = datetime.datetime.now()
        Gametime= aftertime - firstTime
        
        destroyGame()
        a = tkinter.Tk()
        a.geometry("700x350")
        a.title("WINNER")

        label = tkinter.Label(a , text="YOU WIN!\n Timer:"+str(Gametime) ,width=150,height=50,font=("Ariel",30,"bold"),bg="green")
        label.pack()
        saveRecord(str(Gametime))
    

def gameRull():
    global fonts
    global colors
    rand = random.randint(0,100)
    rullS =tkinter.Tk()
    rullS.title("500x500")
    label=tkinter.Label(rullS,text="Try to escape from all the enemies \nthat surround the screen and reach the green ball",font=(fonts[(2*rand)%9],30,"bold"),bg=colors[(3*rand)%50])
    OK = tkinter.Button(rullS, text="Start", command=lambda:( start() , rullS.destroy()),width=20,height=20, font=(fonts[(randFont+3)%10],15,"bold"),bg=colors[(randFont+3)%50])
    label.grid(row=1,column=1)
    OK.grid(row=1,column=2)
def destroyGame():
    root.destroy()


def saveRecord(value):
    global record
    try:
        with open("RecordFile",'x') as file:
            file.write("[record,0]")
        
    except Exception as e:
        root = tkinter.Tk()
        root.geometry("500x200")
        with open("RecordFile",'r') as file:
            prevalue = file.read()
            label=tkinter.Label(root,text="Last record - "+str(prevalue),width=40,height=10,font=("Ariel",12,"bold"))
            label.grid(row=1 , column=0)
            if (prevalue>value):
                va = str(value)
                record = va
                label=tkinter.Label(root,text="scored new record - "+str(record)+" congrate!",font=("Ariel",12,"bold"))
                label.grid(row=0,column=0)
                with open("RecordFile",'w') as file:
                    file.write(va)
    
fonts = ['Arial',
'Helvetica',
'Times New Roman',
'Courier New',
'Verdana',
'Georgia',
'Comic Sans MS',
'Impact',
'Trebuchet MS',
'Palatino']
colors=['bisque', 'blanched almond', 'blue', 'blue violet',
    'brown', 'burlywood', 'cadet blue', 'chartreuse', 'chocolate',
    'coral', 'cornflower blue', 'cornsilk', 'crimson', 'cyan',
    'dark blue', 'dark cyan', 'dark goldenrod', 'dark gray', 'dark green',
    'dark khaki', 'dark magenta', 'dark olive green', 'dark orange', 'dark orchid',
    'dark red', 'dark salmon', 'dark sea green', 'dark slate blue', 'dark slate gray',
    'dark turquoise', 'dark violet', 'deep pink', 'deep sky blue', 'dim gray',
    'dodger blue', 'firebrick', 'floral white', 'forest green', 'fuchsia',
    'gainsboro', 'ghost white', 'gold', 'goldenrod', 'gray',
    'green', 'green yellow', 'honeydew', 'hot pink', 'indian red',
    'indigo', 'ivory', 'khaki', 'lavender', 'lavender blush',
    'lawn green', 'lemon chiffon', 'light blue', 'light coral', 'light cyan']

randFont = random.randint(0,100)

screen_width = screeninfo.get_monitors()[0].width                         
screen_height = screeninfo.get_monitors()[0].height

root = tkinter.Tk()
root.geometry(str(screen_width) + "x" + str(screen_height))
root.title(" ~made by : Sahar~  Game : RedEscape")
root.option_add('*TButton*font', ('Helvetica', 15, 'bold'))
labelTitleGame = tkinter.Label(text="Welcome - Game : RedEscape", width=50, height=10, font=(fonts[randFont%9],15,"bold"),bg=colors[randFont%50])
buttonStart = tkinter.Button(root, text="Start game", command=lambda: start(),width=30,height=10, font=(fonts[(randFont+3)%9],15,"bold"),bg=colors[(randFont+3)%50])
buttonrull = tkinter.Button(root, text="Rull", command=lambda: gameRull(),width=30,height=10, font=(fonts[(randFont+3)%9],15,"bold"),bg=colors[(randFont+3)%50])

labelTitleGame.grid(row=0,column=2)
buttonStart.grid(row=1, column=2)
buttonrull.grid(row=1, column=3)
    
canvas = None
character = None
characterLocation = [0.0,0.0,0.0,0.0]
CoordsEnemys = []
Kgame = [0.0,0.0,0.0,0.0]
firstTime= None
record=0
root.mainloop()
