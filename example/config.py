# -*- coding: utf-8 -*-

def clear_mark_or(combo):
    if isinstance(combo, Key):
        combo = Combo(None, combo)

    def _clear_mark_or():
        if transform._mark_set:
            transform._mark_set = False
            return K("right")
        else:
            return combo

    return _clear_mark_or

def merge(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy,
    second overrides first"""
    z = x.copy()
    z.update(y)
    return z

import re
from xkeysnail.transform import *

# [Global modemap] Change modifier keys as in xmodmap
define_modmap({
    Key.CAPSLOCK: Key.LEFT_CTRL
})

# # [Conditional modmap] Change modifier keys in certain applications
# define_conditional_modmap(re.compile(r'Emacs'), {
#     Key.RIGHT_CTRL: Key.ESC,
# })

# [Multipurpose modmap] Give a key two meanings. A normal key when pressed and
# released, and a modifier key when held down with another key. See Xcape,
# Carabiner and caps2esc for ideas and concept.
# define_multipurpose_modmap(
#     # Enter is enter when pressed and released. Control when held down.
#     {Key.ENTER: [Key.ENTER, Key.RIGHT_CTRL]}

#     # Capslock is escape when pressed and released. Control when held down.
#     # {Key.CAPSLOCK: [Key.ESC, Key.LEFT_CTRL]
#     # To use this example, you can't remap capslock with define_modmap.
# )


## The idea is to make it so that `C-x k k k k` keeps killing tabs
## This is possible with the trick below, but it makes it so that
## the next key pressed is ignored. Not ideal.
# kill_tab = dict()
# kill_tab[K("k")] = [K("C-f4"), kill_tab]

C_x = {
        # C-x h (select all)
        K("h"): [K("C-home"), K("C-a"), set_mark(True)],
        # C-x C-f (open) (I never want to open a file)
        K("C-f"): K("C-o"),
        # C-x C-s (save)
        K("C-s"): K("C-s"),
        # C-x k (kill tab)
        ##K("k"): K("C-f4"),
        K("k"): K("C-f4"), #kill_tab[K("k")],
        # C-x C-c (exit)
        K("C-c"): K("M-f4"),
        # cancel
        K("C-g"): pass_through_key,
        # C-x u (undo)
        K("u"): [K("C-z"), set_mark(False)],
        # C-x p (print)
        K("p"): [K("C-p")],
    }

# Keybindings for Firefox/Chrome
define_keymap(re.compile("Firefox|Google-chrome"), {
    # Ctrl+Alt+j/k to switch next/previous tab
    K("C-Shift-k"): K("C-TAB"),
    K("C-Shift-j"): K("C-Shift-TAB"),
    # Type C-j to focus to the content
    K("M-o"): K("C-f6"),
    # very naive "Edit in editor" feature (just an example)
    # K("C-o"): [K("C-a"), K("C-c"), launch(["gedit"]), sleep(0.5), K("C-v")]
    #
    K("C-x"): merge(C_x, {
        # C-x t (new-tab)
        K("t"): K("C-T"),
        # C-x k (refresh tab)
        K("r"): K("C-r"),
        # C-x b (tab list)
        K("b"): K("C-M-O"),
        # enpass
        K("e"): K("C-slash"),
    })
}, "Firefox and Chrome")

# Keybindings for Zeal https://github.com/zealdocs/zeal/
define_keymap(re.compile("Zeal"), {
    # Ctrl+s to focus search area
    K("C-s"): K("C-k"),
}, "Zeal")

# Emacs-like keybindings in non-Emacs applications
define_keymap(lambda wm_class: wm_class not in ("Gnome-terminal", "Emacs", "URxvt"), {
    # Cursor
    K("C-b"): with_mark(K("left")),
    K("C-f"): with_mark(K("right")),
    K("C-p"): with_mark(K("up")),
    K("C-n"): with_mark(K("down")),
    K("C-t"): with_mark(K("backspace")),
    K("M-t"): with_mark(K("C-backspace")),    
    # Forward/Backward word
    K("M-b"): with_mark(K("C-left")),
    K("M-f"): with_mark(K("C-right")),
    # Beginning/End of line
    K("C-a"): with_mark(K("home")),
    K("C-e"): with_mark(K("end")),
    # Page up/down
    K("M-v"): with_mark(K("page_up")),
    K("C-v"): with_mark(K("page_down")),
    # Beginning/End of file
    K("M-Shift-comma"): with_mark(K("C-home")),
    K("M-Shift-dot"): with_mark(K("C-end")),
    # Newline
    K("C-m"): K("enter"),
    K("C-j"): K("enter"),
    K("C-o"): [K("enter"), K("left")],
    # Copy
    K("C-w"): [K("C-x"), set_mark(False)],
    K("M-w"): [K("C-c"), set_mark(False)],
    K("C-y"): [K("C-v"), set_mark(False)],
    # Delete
    K("C-d"): [K("delete"), set_mark(False)],
    K("M-d"): [K("C-delete"), set_mark(False)],
    # Kill line
    K("C-k"): [K("Shift-end"), K("C-x"), set_mark(False)],
    # Undo
    K("C-slash"): [K("C-z"), set_mark(False)],
    # C-x u (undo)
    K("C-Shift-slash"): [K("C-Shift-z"), set_mark(False)],
    K("C-Shift-ro"): K("C-z"),
    # Mark
    K("C-space"): set_mark(True),
    K("C-M-space"): with_or_set_mark(K("C-right")),
    # Search
    K("C-s"): K("C-f"),
    K("C-r"): K("Shift-F3"),
    K("C-Shift-S"): K("F3"),
    K("M-Shift-key_5"): K("C-h"),
    # Cancel
    K("C-g"): clear_mark_or(K("esc")),
    # Escape
    K("C-q"): escape_next_key,
    # C-x YYY
    K("C-x"): C_x
}, "Emacs-like keys")


define_keymap(lambda wm_class: wm_class in ("Gnome-terminal"), {
    # Cursor
    K("C-t"): with_mark(K("backspace")),
    K("M-t"): with_mark(K("M-backspace")),
    K("M-w"): [K("C-Shift-c")],
    K("C-y"): [K("C-Shift-v")],
    # Cancel
    K("C-q"): escape_next_key,

    K("C-Shift-k"): K("C-page_down"),
    K("C-Shift-j"): K("C-page_up"),

    K("C-x"): {
        K("t"): K("C-Shift-T")}
}, "Emacs-like keys for terminal")


define_keymap(None, {
    # Cursor
    unignore_combo: toggle_ignore_cur_window,
}, "Keymap for all windows")
