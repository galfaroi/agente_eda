---
title: set_global_routing_random(2)
date: 24/09/08
---

# NAME

set_global_routing_random - set global routing random

# SYNOPSIS

set_global_routing_random 
    [-seed seed]
    [-capacities_perturbation_percentage percent]
    [-perturbation_amount value]


# DESCRIPTION

The command randomizes global routing by shuffling the order of the nets
and randomly subtracts or adds to the capacities of a random set of edges. 

Example:
`set_global_routing_random -seed 42 \
  -capacities_perturbation_percentage 50 \
  -perturbation_amount 2`

# OPTIONS

`-seed`:  Sets the random seed (must be non-zero for randomization).

`-capacities_perturbation_percentage`:  Sets the percentage of edges whose capacities are perturbed. By default, the edge capacities are perturbed by adding or subtracting 1 (track) from the original capacity. 

`-perturbation_amount`:  Sets the perturbation value of the edge capacities. This option is only meaningful when `-capacities_perturbation_percentage` is used.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
