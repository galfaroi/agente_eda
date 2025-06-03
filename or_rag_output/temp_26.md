---
title: make_tracks(2)
date: 24/09/08
---

# NAME

make_tracks - make tracks

# SYNOPSIS

make_tracks 
    [layer]
    [-x_pitch x_pitch]
    [-y_pitch y_pitch]
    [-x_offset x_offset]
    [-y_offset y_offset]


# DESCRIPTION

The `initialize_floorplan` command removes existing tracks. 
Use the `make_tracks` command to add routing tracks to a floorplan.

# OPTIONS

`layer`:  Select layer name to make tracks for. Defaults to all layers.

`-x_pitch, -y_pitch`:  If set, overrides the LEF technology x-/y- pitch. Use the same unit as in the LEF file.

`-x_offset, -y_offset`:  If set, overrides the LEF technology x-/y- offset. Use the same unit as in the LEFT file.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
