---
title: set_layer_rc(2)
date: 24/09/08
---

# NAME

set_layer_rc - set layer rc

# SYNOPSIS

set_layer_rc 
    [-layer layer]
    [-via via_layer]
    [-resistance res]
    [-capacitance cap]
    [-corner corner]


# DESCRIPTION

The `set_layer_rc` command can be used to set the resistance and capacitance
for a layer or via. This is useful if these values are missing from the LEF file,
or to override the values in the LEF.

# OPTIONS

`-layer`:  Set layer name to modify. Note that the layer must be a routing layer.

`-via`:  Select via layer name. Note that via resistance is per cut/via, not area-based.

`-resistance`:  Resistance per unit length, same convention as `set_wire_rc`.

`-capacitance`:  Capacitance per unit length, same convention as `set_wire_rc`.

`-corner`:  Process corner to use.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
