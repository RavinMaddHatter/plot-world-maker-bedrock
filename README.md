# plot world maker bedrock
This makes addons for you to deploy on a word. These addons will lock your players in adventure mode unless they were in their automatically assigned plots.

## Getting the release
On the side there is a release section, grab the latest release and download it. Unpack the zip into a folder. That is all that is require, dont move the filed realitive to each other or load these files into minecraft.

## Making a pack
launch the plotzMazer.exe program, Enter the plot X/Z size. Enter the number width of the road between plots. Enter the max number of players. Click the make pack button.


Note: The larger number of plots the more lag that is caused when someone is assigned a plot, Choosing a massive number may not be ideal. This lag is not constant, it occurs when plots are assigned or when players are returned to their plots.

## Setting up the world
Install the pack like a normal addon for the world. Create a flat world with cheats enabled. Enter the world then exit to unlock the "default game mode" option of adventure, this is important for when players are added to the world. Re-Enter the world and run the command below . This world is now ready to play.
```/function startworld```

## Adding a moderator
In my opinion Moderators should have creative privlages i this world globably. To do this have them select a plot like a normal player and then execute the following command (replace the [player name] with the actuall players name.
```/event entity [player name] plotz.removeAll```

## Killing entities
When killing enties, don't run /kill @e, instead run.
```/kill @e[name=!vender] ```
Or set name and or type.


## removing plots from a player
Plots can be removed from a player by doing the following, you have to replace all thigns in the bracket with the correct values:
```
/tag [player name] remove plot[plot number]
/tag [player name] remove plotgiven
/event entity [player name] plotz.removeAll
```
## manually assigning a plot
plots can be manually assigned by usingthe following commands. This can result in 2 players sharing a plot.
 ```
/tag [player name] add plot[plot number]
/tag [player name] add plotgiven
/event entity [player name] plotz.add[plot number]
```
