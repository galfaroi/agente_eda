---
title: gui_select_at(2)
date: 24/09/08
---

# NAME

gui_select_at - gui select at

# SYNOPSIS

gui::select_at 
    x0 y0 x1 y1
    [append]

Or

gui::select_at
    x y 
    [append]


# DESCRIPTION

To add items at a specific point or in an area:

Example usage:
```
gui::select_at x y
gui::select_at x y append
gui::select_at x0 y0 x1 y1
gui::select_at x0 y0 x1 y1 append
```

# OPTIONS

`x, y`:  point in the layout area in microns.

`x0, y0, x1, y1`:  first and second corner of the layout area in microns.

`append`:  if ``true`` (the default value) append the new selections to the current selection list, else replace the selection list with the new selections.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
