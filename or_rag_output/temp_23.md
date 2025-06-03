---
title: set_nets_to_route(2)
date: 24/09/08
---

# NAME

set_nets_to_route - set nets to route

# SYNOPSIS

set_nets_to_route 
    net_names 


# DESCRIPTION

The `set_nets_to_route` command defines a list of nets to route. Only the nets
defined in this command are routed, leaving the remaining nets without any
global route guides.

# OPTIONS

`net_names`:  Tcl list of set of nets (e.g. `{net1, net2}`).

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
