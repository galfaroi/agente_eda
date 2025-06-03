---
title: add_pdn_stripe(2)
date: 24/09/08
---

# NAME

add_pdn_stripe - add pdn stripe

# SYNOPSIS

add_pdn_stripe 
    -layer layer_name
    [-grid grid_name]
    [-width width_value]
    [-followpins]
    [-extend_to_core_ring]
    [-pitch pitch_value]
    [-spacing spacing_value]
    [-offset offset_value]
    [-starts_with POWER|GROUND]
    [-extend_to_boundary]
    [-snap_to_grid]
    [-number_of_straps count]
    [-nets list_of_nets]


# DESCRIPTION

Defines a pattern of power and ground stripes in a single layer to be added to a power grid.

Example usage:

```
add_pdn_stripe -grid main_grid -layer metal1 -followpins
add_pdn_stripe -grid main_grid -layer metal2 -width 0.17 -followpins
add_pdn_stripe -grid main_grid -layer metal4 -width 0.48 -pitch 56.0 -offset 2 -starts_with GROUND
```

# OPTIONS

`-layer`:  Specifies the name of the layer for these stripes.

`-grid`:  Specifies the grid to which this stripe definition will be added. (Default: Last grid defined by `define_pdn_grid`).

`-width`:  Value for the width of stripe.

`-followpins`:  Indicates that the stripe forms part of the stdcell rails, pitch and spacing are dictated by the stdcell rows, the `-width` is not needed if it can be determined from the cells.

`-extend_to_core_ring`:  Extend the stripes to the core PG ring.

`-pitch`:  Value for the distance between each power/ground pair.

`-spacing`:  Optional specification of the spacing between power/ground pairs within a single pitch (Default: pitch / 2).

`-offset`:  Value for the offset of the stripe from the lower left corner of the design core area.

`-starts_with`:  Specifies whether the first strap placed will be POWER or GROUND (Default: grid setting).

`-extend_to_boundary`:  Extend the stripes to the boundary of the grid.

`-snap_to_grid`:  Snap the stripes to the defined routing grid.

`-number_of_straps`:  Number of power/ground pairs to add.

`-nets`:  Limit straps to just this list of nets.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
