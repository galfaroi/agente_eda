---
title: draw_route_guides(2)
date: 24/09/08
---

# NAME

draw_route_guides - draw route guides

# SYNOPSIS

draw_route_guides 
    net_names 
    [-show_pin_locations]


# DESCRIPTION

The `draw_route_guides` command plots the route guides for a set of nets.
To erase the route guides from the GUI, pass an empty list to this command:
`draw_route_guides {}`.

# OPTIONS

`net_names`:  Tcl list of set of nets (e.g. `{net1, net2}`).

`-show_pin_locations`:  Draw circles for the pin positions on the routing grid.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
