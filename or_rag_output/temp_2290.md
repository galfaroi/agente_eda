---
title: create_menu_item(2)
date: 24/09/08
---

# NAME

create_menu_item - create menu item

# SYNOPSIS

create_menu_item 
    [-name name]
    [-path menu_path]
    -text item_text
    -script tcl_script
    [-shortcut key_shortcut] 
    [-echo]


# DESCRIPTION

This command add items to the menubar.
Returns: name of the new item, either ``name`` or ``actionX``.

# OPTIONS

`-name`:  (optional) name of the item, used when deleting the item

`-path`:   (optional) Menu path to place the new item in (hierarchy is separated by /), defaults to "Custom Scripts", but this can also be "Tools" or "New menu/New submenu"

`-text`:  The text to put on the item

`-script`:  The tcl script to evaluate when the button is pressed

`-shortcut`:  (optional) key shortcut to trigger this item

`-echo`:  (optional) indicate that the commands in the ``tcl_script`` should be echoed in the log.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
