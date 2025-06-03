---
title: repair_tie_fanout(2)
date: 24/09/08
---

# NAME

repair_tie_fanout - repair tie fanout

# SYNOPSIS

repair_tie_fanout 
    [-separation dist]
    [-max_fanout fanout]
    [-verbose]
    lib_port


# DESCRIPTION

The `repair_tie_fanout` command connects each tie high/low load to a copy
of the tie high/low cell.

# OPTIONS

`-separation`:  Tie high/low insts are separated from the load by this value (Liberty units, usually microns).

`-verbose`:  Enable verbose logging of repair progress.

`lib_port`:  Tie high/low port, which can be a library/cell/port name or object returned by `get_lib_pins`.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
