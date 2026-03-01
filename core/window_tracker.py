import win32gui

def get_window_rect(title):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        return None
    return win32gui.GetWindowRect(hwnd)