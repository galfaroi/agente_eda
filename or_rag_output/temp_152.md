---
title: place_bondpad(2)
date: 24/09/08
---

# NAME

place_bondpad - place bondpad

# SYNOPSIS

place_bondpad 
    -bond master
    [-offset {x y}]
    [-rotation rotation]
    io_instances


# DESCRIPTION

To place the wirebond pads over the IO cells.

Example usage:

```
place_bondpad -bond PAD IO_*
```

# OPTIONS

`-bond`:  Name of the bondpad master.

`-offset`:  Offset to place the bondpad at with respect to the io instance.

`-rotation`:  Rotation of the bondpad.

`io_instances`:  Names of the instances to add bond pads to.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
