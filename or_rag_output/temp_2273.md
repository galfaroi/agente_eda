---
title: set_global_routing_layer_adjustment(2)
date: 24/09/08
---

# NAME

set_global_routing_layer_adjustment - set global routing layer adjustment

# SYNOPSIS

set_global_routing_layer_adjustment layer adjustment


# DESCRIPTION

The `set_global_routing_layer_adjustment` command sets routing resource
adjustments in the routing layers of the design.  Such adjustments reduce the number of
routing tracks that the global router assumes to exist. This promotes the spreading of routing
and reduces peak congestion, to reduce challenges for detailed routing.

You can set adjustment for a
specific layer, e.g., `set_global_routing_layer_adjustment Metal4 0.5` reduces
the routing resources of routing layer `Metal4` by 50%.  You can also set adjustment
for all layers at once using `*`, e.g., `set_global_routing_layer_adjustment * 0.3` reduces the routing resources of all routing layers by 30%.  And, you can
also set resource adjustment for a layer range, e.g.: `set_global_routing_layer_adjustment
Metal4-Metal8 0.3` reduces the routing resources of routing layers  `Metal4`,
`Metal5`, `Metal6`, `Metal7` and `Metal8` by 30%.

# OPTIONS

`Argument Name`:  Description

`layer`:  Integer for the layer number (e.g. for M1 you would use 1).

`adjustment`:  Float indicating the percentage reduction of each edge in the specified layer.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
