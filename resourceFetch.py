# ============================================
# JAPM (Just Another Program Manager)
# Author: Nayla Hanegan (naylahanegan@gmail.com)
# Date: 9/15/2024
# License: MIT
# ============================================
from pathlib import Path
import sys

def fetchResource(resource_path: Path) -> Path:
    try:  # Running as *.exe; fetch resource from temp directory
        base_path = Path(sys._MEIPASS)
    except AttributeError:  # Running as script; return unmodified path
        return resource_path
    else:   # Return temp resource path
        return base_path.joinpath(resource_path)