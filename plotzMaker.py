import json
from tkinter import StringVar,IntVar, Button,Label,Entry,Tk,DoubleVar, Toplevel,messagebox, ttk
from zipfile import ZipFile
from shutil import copyfile
import os
from os import listdir
from os.path import isfile, join
from os import walk
import glob
import uuid
import shutil

def makepack():
    plotSize=[xsize.get(),zsize.get()]
    pathSize=roadW.get()/2
    maxPlots=plotcount.get()
    with open("playerdefault.json") as f:
        player = json.load(f)
    packName="plots for {} players, size {}x{}, path {}".format(maxPlots,xsize.get(),zsize.get(),int(pathSize*2))
    x = 0
    y = 0
    dx = 0
    dy = -1
    aniName="controller.animation.plotz.controller"
    aniC={"format_version": "1.10.0"}
    aniC["animation_controllers"]={
        aniName: {
            "initial_state": "default",
                "states": {}}}
    player["minecraft:entity"]["description"]["animations"]={"pltzctrl":aniName}
    player["minecraft:entity"]["description"]["scripts"]={"animate":["pltzctrl"]}
    player["minecraft:entity"]["component_groups"]["plotz.none"]={"minecraft:variant":{"value":0}}
    states={}
    setup=["summon armor_stand 0 4 0 hi vender\n",
           "setworldspawn 0 4 7\n",
           "tp @a 0 4 7\n",
           "gamerule spawnradius 1\n",
           "structure load plotsvender -1 3 -1\n",
           "gamerule showcoordinates true\n",
           "scoreboard objectives add plot dummy plot\n",
           "scoreboard players set @e[name=vender] plot 0\n",
           "gamerule showcoordinates true\n",
           "gamerule firedamage false\n",
           "gamerule pvp false\n",
           "gamerule falldamage false\n",
           "gamerule doinsomnia false\n",
           "gamerule mobgriefing false\n",
           "gamerule domobspawning false\n",
           "gamerule tntexplodes false\n",
           "gamerule dofiretick false\n",
           "gamerule keepinventory false\n",
           "gamerule drowningdamage true"]
    
    givePlot=["execute @e[name=vender] ~~~ execute @p[tag=!plotgiven,r=5] ~~~ scoreboard players add @e[r=5,name=vender] plot 1\n"]
    givePlot.append("execute @e[name=vender] ~~~ w @p[tag=!plotgiven,r=5] You have been tp'ed to your plot, if you get lost go back to 0,0 and click the button to get back\n")
    
    givePlot.append("execute @e[name=vender] ~~~ tag @p[tag=!plotgiven,r=5] add giveplot\n")
    
    for i in range(maxPlots):
        if (-int(pow(maxPlots,0.5))/2 < x <= int(pow(maxPlots,0.5))/2) and (-int(pow(maxPlots,0.5))/2 < y <= int(pow(maxPlots,0.5)/2)):
            if i==0:
                states["default"]={}
                states["default"]["on_entry"]=["/gamemode a"]
                states["default"]["transitions"]=[]
                player["minecraft:entity"]["events"]["plotz.removeAll"]={"remove":{"component_groups":[]}}
                player["minecraft:entity"]["events"]["plotz.removeAll"]["add"]={"component_groups":["plotz.none"]}
            if i>0:
                
                inplotName="plot{}in".format(i)
                outplotName="plot{}out".format(i)
                compName="plotz.plot{}".format(i)
                addEvent="plotz.add{}".format(i)
                xcenter = (plotSize[0] + 2 * pathSize) * x
                ycenter = (plotSize[1] + 2 * pathSize) * y
                givePlot.append("execute @e[name=vender,scores={plot="+str(i)+"}] ~~~ event entity @p[tag=!plotgiven,r=5] "+addEvent+"\n")
                givePlot.append("execute @e[name=vender,scores={plot="+str(i)+"}"+"] ~~~ tag @p[tag=!plotgiven,r=5] add plot{}\n".format(i))
                givePlot.append("execute @e[name=vender] ~~~ tp @p[tag=plot{},r=5] {} 4 {}\n".format(i,xcenter-plotSize[0]/2,ycenter-plotSize[1]/2))
                
                xmin=(plotSize[0] + 2*pathSize)*x-plotSize[0]/2#+pathSize/2
                xmax=(plotSize[0] + 2*pathSize)*x+plotSize[0]/2#-pathSize/2
                ymin=(plotSize[1] + 2*pathSize)*y-plotSize[1]/2#+pathSize/2
                ymax=(plotSize[1] + 2*pathSize)*y+plotSize[1]/2#-pathSize/2
                plotText = ("Your Plot is at X: {}, Z: {}".format(xcenter,ycenter))
                inplot=("query.position(0)<{}&&query.position(0)>{}&&query.position(2)>{}&&query.position(2)<{}".format(xmax,xmin,ymin,ymax))
                outplot=("query.position(0)>{}||query.position(0)<{}||query.position(2)<{}||query.position(2)>{}".format(xmax,xmin,ymin,ymax))
                
                
                plotcmd="query.variant=={}".format(i)
                plotoutcmd="query.variant!={}".format(i)
                states["default"]["transitions"].append({outplotName:plotcmd})
                states[outplotName]={}
                states[outplotName]["transitions"]=[{"default":plotoutcmd}]
                states[outplotName]["transitions"].append({inplotName:inplot})
                states[outplotName]["on_entry"]=["/gamemode a","/w @s you were given plot {}".format(i),"/w @s {}".format(plotText)]
                states[inplotName]={}
                states[inplotName]["transitions"]=[{"default":plotoutcmd}]
                states[inplotName]["transitions"].append({outplotName:outplot})
                states[inplotName]["on_exit"]=["/clear @s\n"]
                states[inplotName]["on_exit"].append("/replaceitem entity @s slot.armor.chest 0 elytra\n")
                states[inplotName]["on_exit"].append("/give @s firework_rocket 64\n")
                states[inplotName]["on_entry"]=["/gamemode c"]
                
                player["minecraft:entity"]["component_groups"][compName]={}
                player["minecraft:entity"]["component_groups"][compName]={"minecraft:variant":{"value":i}}
                player["minecraft:entity"]["events"]["plotz.removeAll"]["remove"]["component_groups"].append(compName)
                player["minecraft:entity"]["events"][addEvent]={"add":{"component_groups":[compName]}}
                
                
            # DO STUFF...
        if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
            dx, dy = -dy, dx
        x, y = x+dx, y+dy
    givePlot.append("tag @p[tag=giveplot] add plotgiven\n")
    givePlot.append("execute @p[tag=giveplot]  ~ ~ ~ fill ~ ~-1 ~ ~{} ~-1 ~{} quartz_bricks\n".format(int(plotSize[0]),int(plotSize[1])))
    givePlot.append("execute @p[tag=giveplot]  ~ ~ ~ fill ~+1 ~-1 ~+1 ~{} ~-1 ~{} grass\n".format(int(plotSize[0]-1),int(plotSize[1]-1)))
    givePlot.append("tag @a[tag=giveplot] remove giveplot\n")
    aniC["animation_controllers"][aniName]["states"]=states
    aniPath=os.path.join(packName,"entities","player.json")
    os.makedirs(os.path.dirname(aniPath), exist_ok=True)
    with open(aniPath, "w+") as json_file:
        json.dump(player, json_file, indent=2)
    acpath=os.path.join(packName,"animation_controllers","plotz.json")
    os.makedirs(os.path.dirname(acpath), exist_ok=True)
    with open(acpath, "w+") as json_file:
        json.dump(aniC, json_file, indent=2)
    givePlotPath=os.path.join(packName,"functions","giveplot.mcfunction")
    os.makedirs(os.path.dirname(givePlotPath), exist_ok=True)
    with open(givePlotPath, "w+") as functionFile:
        for line in givePlot:
            functionFile.write(line)
    startPath=os.path.join(packName,"functions","startworld.mcfunction")
    os.makedirs(os.path.dirname(startPath), exist_ok=True)
    with open(startPath, "w+") as functionFile:
        for line in setup:
            functionFile.write(line)
    pathtoStructure=os.path.join(packName,"structures","plotsvender.mcstructure")
    os.makedirs(os.path.dirname(pathtoStructure), exist_ok=True)
    
    copyfile("plotsvender.mcstructure",pathtoStructure)
    pathtoStructure=os.path.join(packName,"pack_icon.png")
    copyfile("pack_icon.png",pathtoStructure)
    manifest={"format_version": 2,"header": {},"modules": []}
    manifest["header"]["name"]=packName
    manifest["header"]["description"]=packName
    manifest["header"]["uuid"]= str(uuid.uuid4())
    manifest["header"]["version"]=[0,0,1]
    manifest["header"]["min_engine_version"]=[1,16,1]
    manifest["modules"].append({"type": "data",
                                "uuid":str(uuid.uuid4()),
                                           "version": [1,0,0]})
    pathToMani=os.path.join(packName,"manifest.json")
    os.makedirs(os.path.dirname(pathToMani), exist_ok=True)
    with open(pathToMani, "w+") as json_file:
        json.dump(manifest, json_file, indent=2)
    file_paths = []
    for directory,_,_ in os.walk(packName):
        file_paths.extend(glob.glob(os.path.join(directory, "*.*")))
    with ZipFile("{}.mcaddon".format(packName), 'x') as zip:
        for file in file_paths:
            print(file)
            zip.write(file)
    shutil.rmtree(packName)
                
root = Tk()
root.title("Madhatter's Plot World Maker")
xsizeLb=Label(root, text="X size")
zsizeLb=Label(root, text="Z size")
roadWLb=Label(root, text="Road Width")
totalPlotsLb=Label(root, text="Total Plots")

xsize=IntVar()
xsize.set(16)
zsize=IntVar()
zsize.set(16)
roadW=IntVar()
roadW.set(8)
plotcount=IntVar()
plotcount.set(32)
xsizeEntry = Entry(root,textvariable=xsize)
zsizeEntry = Entry(root,textvariable=zsize)
roadWEntry = Entry(root,textvariable=roadW)
plotcountEntry = Entry(root,textvariable=plotcount)
saveButton=Button(root,text="Make Pack",command=makepack)
r=0
xsizeEntry.grid(row=r,column=1)
xsizeLb.grid(row=r,column=0)
r+=1
zsizeEntry.grid(row=r,column=1)
zsizeLb.grid(row=r,column=0)
r+=1
roadWEntry.grid(row=r,column=1)
roadWLb.grid(row=r,column=0)
r+=1
plotcountEntry.grid(row=r,column=1)
totalPlotsLb.grid(row=r,column=0)
r+=1
saveButton.grid(row=r,column=0)
root.mainloop(  )
root.quit()
