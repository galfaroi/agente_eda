---
title: report_wire_length(2)
date: 24/09/08
---

# NAME

report_wire_length - report wire length

# SYNOPSIS

report_wire_length 
    [-net net_list]
    [-file file]
    [-global_route]
    [-detailed_route]
    [-verbose]


# DESCRIPTION

The `report_wire_length` command reports the wire length of the nets. Use the `-global_route`
and the `-detailed_route` flags to report the wire length from global and detailed routing,
respectively. If none of these flags are used, the tool will identify the state of the design
and report the wire length accordingly.

Example: `report_wire_length -net {clk net60} -global_route -detailed_route -verbose -file out.csv`

# OPTIONS

`-net`:  List of nets to report the wirelength. Use `*` to report the wire length for all nets of the design.

`-file`:  The name of the file for the wirelength report.

`-global_route`:  Report the wire length of the global routing.

`-detailed_route`:  Report the wire length of the detailed routing.

`-verbose`:  This flag enables the full reporting of the layer-wise wirelength information.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
