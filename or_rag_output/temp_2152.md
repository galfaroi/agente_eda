---
title: gui_set_display_controls(2)
date: 24/09/08
---

# NAME

gui_set_display_controls - gui set display controls

# SYNOPSIS

gui::set_display_controls 
    name 
    [display_type] 
    [value]


# DESCRIPTION

Control the visible and selected elements in the layout:

# OPTIONS

`name`:   is the name of the control. For example, for the power nets option this would be ``Signals/Power`` or could be ``Layers/*`` to set the option for all the layers.

`display_type`:  is either ``visible`` or ``selectable``

`value`: is either ``true`` or ``false``

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
