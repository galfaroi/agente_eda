---
title: write_pg_spice(2)
date: 24/09/08
---

# NAME

write_pg_spice - write pg spice

# SYNOPSIS

write_pg_spice
    -net net_name
    [-vsrc vsrc_file]
    [-corner corner]
    [-source_type FULL|BUMPS|STRAPS]
    spice_file


# DESCRIPTION

This command writes the `spice` file for power grid.

# OPTIONS

`-net`:  Name of the net to analyze. Must be a power or ground net name.

`-vsrc`:  File to set the location of the power C4 bumps/IO pins. See [Vsrc_aes.loc file](test/Vsrc_aes_vdd.loc) for an example and its [description](doc/Vsrc_description.md).

`-corner`:  Corner to use for analysis.

`-source_type`:  Indicate the type of voltage source grid to [model](#source-grid-options). FULL uses all the nodes on the top layer as voltage sources, BUMPS will model a bump grid array, and STRAPS will model power straps on the layer above the top layer.

`spice_file`:  File to write spice netlist to.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
