---
title: gui_add_ruler(2)
date: 24/09/08
---

# NAME

gui_add_ruler - gui add ruler

# SYNOPSIS

gui::add_ruler 
    x0 y0 x1 y1
    [label]
    [name]
    [euclidian]


# DESCRIPTION

To add a ruler to the layout:

1. either press ``k`` and use the mouse to place it visually.
To disable snapping for the ruler when adding, hold the ``Ctrl`` key, and to allow non-horizontal or vertical snapping when completing the ruler hold the ``Shift`` key.

2. or use the command:

Returns: name of the newly created ruler.

# OPTIONS

`x0, y0, x1, y1`:  first and second end point of the ruler in microns.

`label`:  text label for the ruler.

`name`:  name of the ruler.

`euclidian`:  ``1`` for euclidian ruler, and ``0`` for regular ruler.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
