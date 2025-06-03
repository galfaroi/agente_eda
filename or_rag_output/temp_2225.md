---
title: check_power_grid(2)
date: 24/09/08
---

# NAME

check_power_grid - check power grid

# SYNOPSIS

check_power_grid
    -net net_name
    [-floorplanning]
    [-error_file error_file]


# DESCRIPTION

This command checks power grid.

# OPTIONS

`-net`:  Name of the net to analyze. Must be a power or ground net name.

`-floorplanning`:  Ignore non-fixed instances in the power grid, this is useful during floorplanning analysis when instances may not be properly placed.

`-error_file`:  File to write power grid errors to.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
