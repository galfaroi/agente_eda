---
title: add_sroute_connect(2)
date: 24/09/08
---

# NAME

add_sroute_connect - add sroute connect

# SYNOPSIS

add_sroute_connect
    -layers list_of_2_layers
    -cut_pitch pitch_value
    [-net net]
    [-outerNet outerNet]
    [-fixed_vias list_of_vias]
    [-max_rows rows]
    [-max_columns columns]
    [-metalwidths metalwidths]
    [-metalspaces metalspaces]
    [-ongrid ongrid_layers]
    [-insts inst]


# DESCRIPTION

The `add_sroute_connect` command is employed for connecting pins located
outside of a specific power domain to the power ring, especially in cases where
multiple power domains are present. During `sroute`, multi-cut vias will be added
for new connections. The use of fixed vias from the technology file should be
specified for the connection using the `add_sroute_connect` command. The use
of max_rows and max_columns defines the row and column limit for the via stack.

Example:
```
add_sroute_connect  -net "VIN" -outerNet "VDD" -layers {met1 met4} -cut_pitch {200 200} -fixed_vias {M3M4_PR_M} -metalwidths {1000 1000} -metalspaces {800} -ongrid {met3 met4} -insts "temp_analog_1.a_header_0"
```

# OPTIONS

`-net`:  The inner net where the power ring exists.

`-outerNet`:  The outer net where instances/pins that need to get connected exist.

`-layers`:   The metal layers for vertical stripes within inner power ring.

`-cut_pitch`:  Distance between via cuts when the two layers are parallel, e.g., overlapping stdcell rails. (Default:200 200)

`-fixed_vias`:  List of fixed vias to be used to form the via stack.

`-max_rows`:  Maximum number of rows when adding arrays of vias. (Default:10)

`-max_columns`:  Maximum number of columns when adding arrays of vias. (Default:10)

`-metalwidths`:  Width for each metal layer.

`-metalspaces`:  Spacing of each metal layer.

`-ongrid`:  List of intermediate layers in a via stack to snap onto a routing grid.

`-insts`:  List of all the instances that contain the pin that needs to get connected with power ring. (Default:nothing)

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
