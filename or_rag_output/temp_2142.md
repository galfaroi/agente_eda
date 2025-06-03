---
title: place_io_terminals(2)
date: 24/09/08
---

# NAME

place_io_terminals - place io terminals

# SYNOPSIS

place_io_terminals
    -allow_non_top_layer
    inst_pins


# DESCRIPTION

In the case where the bond pads are integrated into the padcell, the IO terminals need to be placed.
This command place terminals on the padring.

Example usage: 
```
place_io_terminals u_*/PAD
place_io_terminals u_*/VDD
```

# OPTIONS

`-allow_non_top_layer`:  Allow the terminal to be placed below the top layer.

`inst_pins`:  Instance pins to place the terminals on.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
