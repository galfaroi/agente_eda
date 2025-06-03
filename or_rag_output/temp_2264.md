---
title: add_pdn_connect(2)
date: 24/09/08
---

# NAME

add_pdn_connect - add pdn connect

# SYNOPSIS

add_pdn_connect 
    -layers list_of_two_layers
    [-grid grid_name]
    [-cut_pitch pitch_value]
    [-fixed_vias list_of_fixed_vias]
    [-dont_use_vias list_of_vias]
    [-max_rows rows]
    [-max_columns columns]
    [-ongrid ongrid_layers]
    [-split_cuts split_cuts_mapping]


# DESCRIPTION

The `add_pdn_connect` command is used to define which layers in the power grid are to be connected together. During power grid generation, vias will be added for overlapping power nets and overlapping ground nets. The use of fixed vias from the technology file can be specified or else via stacks will be constructed using VIARULEs. If VIARULEs are not available in the technology, then fixed vias must be used.

Example usage:

```
add_pdn_connect -grid main_grid -layers {metal1 metal2} -cut_pitch 0.16
add_pdn_connect -grid main_grid -layers {metal2 metal4}
add_pdn_connect -grid main_grid -layers {metal4 metal7}

add_pdn_connect -grid ram -layers {metal4 metal5}
add_pdn_connect -grid ram -layers {metal5 metal6}
add_pdn_connect -grid ram -layers {metal6 metal7}

add_pdn_connect -grid rotated_rams -layers {metal4 metal6}
add_pdn_connect -grid rotated_rams -layers {metal6 metal7}
```

# OPTIONS

`-layers`:  Layers to be connected where there are overlapping power or overlapping ground nets.

`-grid`:  Specifies the name of the grid definition to which this connection will be added (Default: Last grid created by `define_pdn_grid`).

`-cut_pitch`:  When the two layers are parallel e.g. overlapping stdcell rails, specify the distance between via cuts.

`-fixed_vias`:  List of fixed vias to be used to form the via stack.

`-dont_use_vias`:  List or pattern of vias to not use to form the via stack.

`-max_rows`:  Maximum number of rows when adding arrays of vias.

`-max_columns`:  Maximum number of columns when adding arrays of vias.

`-ongrid`:  List of intermediate layers in a via stack to snap onto a routing grid.

`-split_cuts`:  Specifies layers to use split cuts on with an associated pitch, for example `{metal3 0.380 metal5 0.500}`.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
