---
title: add_pdn_ring(2)
date: 24/09/08
---

# NAME

add_pdn_ring - add pdn ring

# SYNOPSIS

add_pdn_ring 
    -layers layer_name
    -widths width_value|list_of_2_values
    -spacings spacing_value|list_of_2_values
    [-grid grid_name]
    [-core_offsets offset_value]
    [-pad_offsets offset_value]
    [-add_connect]
    [-extend_to_boundary]
    [-connect_to_pads]
    [-connect_to_pad_layers layers]
    [-starts_with POWER|GROUND]
    [-nets list_of_nets]
    [-ground_pads pads]
    [-power_pads pads]



# DESCRIPTION

The `add_pdn_ring` command is used to define power/ground rings around a grid region.
The ring structure is built using two layers that are orthogonal to each other.
A power/ground pair will be added above and below the grid using the horizontal
layer, with another power/ground pair to the left and right using the vertical layer.
Together these 4 pairs of power/ground stripes form a ring around the specified grid.
Power straps on these layers that are inside the enclosed region are extend to 
connect to the ring.

Example usage: 

```
add_pdn_ring -grid main_grid -layer {metal6 metal7} -widths 5.0 -spacings  3.0 -core_offset 5
```

# OPTIONS

`-layers`:  Specifies the name of the layer for these stripes.

`-widths`:  Value for the width of the stdcell rail.

`-spacings`:  Optional specification of the spacing between power/ground pairs within a single pitch. (Default: pitch / 2).

`-grid`:  Specifies the name of the grid to which this ring defintion will be added. (Default: Last grid created by `define_pdn_grid`).

`-core_offsets`:  Value for the offset of the ring from the grid region.

`-pad_offsets`:  When defining a power grid for the top level of an SoC, can be used to define the offset of ring from the pad cells.

`-add_connect`:  Automatically add a connection between the two layers.

`-extend_to_boundary`:  Extend the rings to the grid boundary.

`-connect_to_pads`:  The core side of the pad pins will be connected to the ring.

`-connect_to_pad_layers`:  Restrict the pad pins layers to this list.

`-starts_with`:  Specifies whether the first strap placed will be POWER or GROUND (Default: grid setting).

`-nets`:  Limit straps to just this list of nets.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
