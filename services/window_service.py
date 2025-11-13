import pygetwindow as gw

def get_active_window():
    try:
        focus = gw.getActiveWindow()
        if focus:
            return focus.title
        return "N/A"
    except Exception:
        return "ERRO_JANELA"  