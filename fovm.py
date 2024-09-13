import win32gui
import win32con
import dearpygui.dearpygui as dpg
import ctypes
from ctypes import c_int
import time
import keyboard

# Initialize DWM API
dwm = ctypes.windll.dwmapi

# Define MARGINS class
class MARGINS(ctypes.Structure):
    _fields_ = [("cxLeftWidth", c_int),
                ("cxRightWidth", c_int),
                ("cyTopHeight", c_int),
                ("cyBottomHeight", c_int)]

# Setup Dear PyGui
dpg.create_context()
dpg.create_viewport(title='overlay', always_on_top=True, decorated=False, clear_color=[0.0, 0.0, 0.0, 0.0])
dpg.set_viewport_always_top(True)
dpg.setup_dearpygui()

# Create a viewport drawlist for drawing the FOV circle
dpg.add_viewport_drawlist(front=False, tag="Viewport_back")

# Initialize global variables
circle = None

# FOV Circle drawing function
def update_fov_circle():
    global circle
    if dpg.get_value(check1):
        fov_value = dpg.get_value(slider1)
        if circle is not None:
            dpg.delete_item(circle)
        circle = dpg.draw_circle((960, 540), fov_value, color=(255, 255, 255, 255), parent="Viewport_back")
    else:
        if circle is not None:
            dpg.delete_item(circle)
            circle = None

# Create GUI components
with dpg.window(label="Fov Menu", width=200, height=300):
    check1 = dpg.add_checkbox(label="Show Fov", callback=lambda: update_fov_circle())
    slider1 = dpg.add_slider_float(label="Fov", min_value=25, max_value=150, default_value=25, callback=lambda: update_fov_circle())

dpg.show_viewport()
dpg.toggle_viewport_fullscreen()

# Get the window handle and initialize click-through state
hwnd = win32gui.FindWindow(None, "overlay")
margins = MARGINS(-1, -1, -1, -1)
dwm.DwmExtendFrameIntoClientArea(hwnd, margins)

# Initialize click-through state
click_through = False
original_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)

def apply_click_through():
    style = original_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)

def remove_click_through():
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, original_style)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)

# Main loop
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

    # Toggle click-through on F8 key press
    if keyboard.is_pressed('F8'):
        click_through = not click_through
        if click_through:
            apply_click_through()
        else:
            remove_click_through()
        time.sleep(0.2)  # Small delay to prevent rapid toggling

# Cleanup
dpg.destroy_context()
