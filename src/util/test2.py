# import Xlib
# from Xlib import display
# from Xlib import X

# print(X.PointerMotionMask)

import Xlib
import Xlib.display

disp = Xlib.display.Display()
Xroot = disp.screen().root
NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
Xroot.change_attributes(event_mask=Xlib.X.PropertyChangeMask |
                        Xlib.X.SubstructureNotifyMask)

windows = []

while True:
    # loop until an event happens that we care about
    # we care about a change to which window is active
    # (NET_ACTIVE_WINDOW property changes on the root)
    # or about the currently active window changing
    # in size or position (ConfigureNotify event for
    # our window or one of its ancestors)
    event = disp.next_event()
    if (event.type == Xlib.X.PropertyNotify and event.atom == NET_ACTIVE_WINDOW):
        active = disp.get_input_focus().focus
        try:
            name = active.get_wm_class()[1]
        except TypeError:
            name = "unknown"
        print("The active window has changed! It is now", name)

        # Because an X window is not necessarily just what one thinks of
        # as a window (the window manager may add an invisible frame, and
        # so on), we record not just the active window but its ancestors
        # up to the root, and treat a ConfigureNotify on any of those
        # ancestors as meaning that the active window has been moved or resized
        pointer = active
        windows = []
        while pointer.id != Xroot.id:
            windows.append(pointer)
            pointer = pointer.query_tree().parent
    elif event.type == Xlib.X.ConfigureNotify and event.window in windows:
        print("Active window size/position is now", event.x, event.y,
              event.width, event.height)