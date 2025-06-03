---
title: set_routing_layers(2)
date: 24/09/08
---

# NAME

set_routing_layers - set routing layers

# SYNOPSIS

set_routing_layers 
    [-signal min-max]
    [-clock min-max]


# DESCRIPTION

This command sets the minimum and maximum routing layers for signal and clock nets.
Example: `set_routing_layers -signal Metal2-Metal10 -clock Metal6-Metal9`

# OPTIONS

`-signal`:  Set the min and max routing signal layer (names) in this format "%s-%s".

`-clock`:  Set the min and max routing clock layer (names) in this format "%s-%s".

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
