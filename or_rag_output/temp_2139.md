---
title: analyze_power_grid(2)
date: 24/09/08
---

# NAME

analyze_power_grid - analyze power grid

# SYNOPSIS

analyze_power_grid
    -net net_name
    [-corner corner]
    [-error_file error_file]
    [-voltage_file voltage_file]
    [-enable_em]
    [-em_outfile em_file]
    [-vsrc voltage_source_file]
    [-source_type FULL|BUMPS|STRAPS]


# DESCRIPTION

This command analyzes power grid.

# OPTIONS

`-net`:  Name of the net to analyze, power or ground net name.

`-corner`:  Corner to use for analysis.

`-error_file`:  File to write power grid error to.

`-vsrc`:  File to set the location of the power C4 bumps/IO pins. [Vsrc_aes.loc file](test/Vsrc_aes_vdd.loc) for an example with a description specified [here](doc/Vsrc_description.md).

`-enable_em`:  Report current per power grid segment.

`-em_outfile`:  Write the per-segment current values into a file. This option is only available if used in combination with `-enable_em`.

`-voltage_file`:  Write per-instance voltage into the file.

`-source_type`:  Indicate the type of voltage source grid to [model](#source-grid-options). FULL uses all the nodes on the top layer as voltage sources, BUMPS will model a bump grid array, and STRAPS will model power straps on the layer above the top layer.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
