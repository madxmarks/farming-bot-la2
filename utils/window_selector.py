import win32gui

def list_windows():
    result = []

    def enum_handler(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                result.append((title, hwnd))

    win32gui.EnumWindows(enum_handler, None)
    return result