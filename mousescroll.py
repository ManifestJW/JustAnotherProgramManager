# ============================================
# JAPM (Just Another Program Manager)
# Author: Nayla Hanegan (naylahanegan@gmail.com)
# Date: 9/15/2024
# License: MIT
# ============================================
import sys

def bind_mouse_wheel(canvas):
    """Bind mouse wheel events for scrolling."""
    def on_mouse_wheel(event):
        if sys.platform == "darwin":  # macOS
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:  # Windows and other platforms
            canvas.yview_scroll(int(-1 * (event.delta)), "units")

    # Bind the appropriate mouse wheel event
    canvas.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))  # Scroll up
    canvas.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))  # Scroll down
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Bind mouse wheel event to the canvas

