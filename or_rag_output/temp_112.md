---
title: set_global_routing_region_adjustment(2)
date: 24/09/08
---

# NAME

set_global_routing_region_adjustment - set global routing region adjustment

# SYNOPSIS

set_global_routing_region_adjustment
    {lower_left_x lower_left_y upper_right_x upper_right_y}
    -layer layer 
    -adjustment adjustment


# DESCRIPTION

Set global routing region adjustment.
Example: `set_global_routing_region_adjustment {1.5 2 20 30.5} -layer Metal4 -adjustment 0.7`

# OPTIONS

`lower_left_x, lower_left_y, upper_right_x , upper_right_y`:  Bounding box to consider.

`-layer`:  Integer for the layer number (e.g. for M1 you would use 1).

`-adjustment`:  Float indicating the percentage reduction of each edge in the specified layer.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
