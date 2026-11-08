All Credits to SCLERA npo : https://sclera.be/en/vzw/home 
# Steps 
- Note: You have to change paht names in scrpts. 
## Translation 
* Open the PNGs folder in a Web browser as Chrome.
* Copy the list of file names 
* You can use Notepad++, paste the text and use with alt+shift+ mouse for selecting only the text you want. 
* Then translate the folder with Chrome translator. 
* Copy the new list of names. 
* Use Renombrar.ps1 PowerShell script for change names. 
## Creating SVGs 
* You will need "FontForge", install it. Then you have to download "Potrace.exe" and paste it in the PNGs folder 
* Use PNGtoSVG.py in phyton IDLE for creating SVGs folder. (This script only works with black and white colors and inverts the Sclera's images colors for eliminate contrast) 
## Creating Fonts 
* Use script.py with phyton IDLE for creating fonts. 
* Use jsoncreator_v2.py for creatings sclera_maps.json.
