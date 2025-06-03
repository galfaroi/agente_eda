---
title: insert_decap(2)
date: 24/09/08
---

# NAME

insert_decap - insert decap

# SYNOPSIS

insert_decap -target_cap target_cap [-net net_name] -cells list_of_decap_with_cap


# DESCRIPTION

The `insert_decap` command inserts decap cells in the areas with the highest
IR Drop. The number of decap cells inserted will be limited to the target
capacitance defined in the `-target_cap` option. `list_of_decap_with_cap`
is a list of even size of decap master cells and their capacitances,
e.g., `<cell1> <decap_of_cell1> <cell2> <decap_of_cell2> ...`. To insert decap
cells in the IR Drop of a specific net (power or ground) use `-net <net_name>`,
if not defined the default power net will be used.
To use this command, you must first execute the `analyze_power_grid` command
with the net to have the IR Drop information.

# OPTIONS

`-target_cap`:  Target capacitance to insert os decap cells.

`-net`:  Power or ground net name. The decap cells will be inserted near the IR Drops of the net.

`-cells`:  List of even size of decap master cells and their capacitances.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
