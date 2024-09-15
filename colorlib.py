# ============================================
# JAPM (Just Another Program Manager)
# Author: Nayla Hanegan (naylahanegan@gmail.com)
# Date: 9/14/2024
# License: MIT
# ============================================
import sys
import subprocess

if sys.platform == "win32":
    from get_system_color import *


def darken_color(r,g,b, factor):
    return [r*factor, g*factor, b*factor]


def get_system_colors():
    if sys.platform == "darwin":
        try:
            sysColor = subprocess.run(["defaults", "read", "-g", "AppleAccentColor"], capture_output=True, text=True)
            sysColor = sysColor.stdout.strip()
        except:
            sysColor = "7"
        if sysColor == "6":
            sysColor = "#f74f9e" # Pink
            sysColorAlt = "#c42b66"
        elif sysColor == "5":
            sysColor = "#a550a7" # Purple
            sysColorAlt = "#863b7f"
        elif sysColor == "4" or sysColor == "7":
            sysColor = "#007aff" # Blue
            sysColorAlt = "#0054b3"
        elif sysColor == "3":
            sysColor = "#62ba46" # Green
            sysColorAlt = "#4f9e37"
        elif sysColor == "2":
            sysColor = "#ffc600" # Yellow
            sysColorAlt = "#cc9200"
        elif sysColor == "1": 
            sysColor = "#f7821b" # Orange
            sysColorAlt = "#ae5b14"
        elif sysColor == "0": 
            sysColor = "#ff5257" # Red
            sysColorAlt = "#cc2c30"
        elif sysColor == "-1":
            sysColor = "#8c8c8c" # Graphite
            sysColorAlt = "#5c5c5c"
            
    elif sys.platform == "win32":
        sysColor = get_windows_system_color()[4]
        sysColor1 = get_windows_system_color()[0]
        sysColor2 = get_windows_system_color()[1]
        sysColor3 = get_windows_system_color()[2]
        sysColorAlt = darken_color(sysColor1, sysColor2, sysColor3, 0.75)
        sysColorAlt = "#{0:02x}{1:02x}{2:02x}".format(int(sysColorAlt[0]), int(sysColorAlt[1]), int(sysColorAlt[2]))

    return sysColor, sysColorAlt