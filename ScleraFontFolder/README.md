# Sclera Font Folder

All credits for the original pictograms go to Sclera NPO:
https://sclera.be/en/vzw/home

## Requirements

- Python and Python IDLE.
- FontForge.
- Potrace ("potrace.exe").
- Google Chrome.
- Notepad++ (optional).

Note: You may need to adjust file and folder paths in the scripts before running them.

1. Translating the PNG filenames

1. Open the "PNGs" folder in Google Chrome or another web browser.
2. Copy the list of filenames.
3. Paste the list into Notepad++.
4. Use "Alt + Shift + Mouse Selection" to select and copy only the text you need.
5. Use Chrome's translation feature to translate the filenames.
6. Copy the translated list.
7. Run "Renombrar.ps1" using PowerShell to rename the files.

2. Creating SVG files

1. Install FontForge.
2. Download "potrace.exe" and place it inside the "PNGs" folder.
3. Run "PNGtoSVG.py" using Python IDLE.
4. The script will generate an "SVGs" folder.

Important: The conversion script only works with black-and-white images. It also inverts the colors of Sclera's images to eliminate contrast.

3. Creating the font

Run "script.py" using Python IDLE to generate the font files.

4. Creating the JSON dictionary

Run "jsoncreator_v2.py" to generate "sclera_maps.json".
