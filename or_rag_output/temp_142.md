---
title: gui_set_heatmap(2)
date: 24/09/08
---

# NAME

gui_set_heatmap - gui set heatmap

# SYNOPSIS

gui::set_heatmap 
    name
    [option]
    [value]


# DESCRIPTION

To control the settings in the heat maps:

The currently availble heat maps are:
- ``Power``
- ``Routing``
- ``Placement``
- ``IRDrop``
- ``RUDY`` [^RUDY]

These options can also be modified in the GUI by double-clicking the underlined display control for the heat map.

# OPTIONS

`name`:  is the name of the heatmap.

`option`:  is the name of the option to modify. If option is ``rebuild`` the map will be destroyed and rebuilt.

`value`:  is the new value for the specified option. This is not used when rebuilding map.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
