---
title: buffer_ports(2)
date: 24/09/08
---

# NAME

buffer_ports - buffer ports

# SYNOPSIS

buffer_ports 
    [-inputs] 
    [-outputs] 
    [-max_utilization util]
    [-buffer_cell buf_cell]


# DESCRIPTION

The `buffer_ports -inputs` command adds a buffer between the input and its
loads.  The `buffer_ports -outputs` adds a buffer between the port driver
and the output port. Inserting buffers on input and output ports makes
the block input capacitances and output drives independent of the block
internals.

# OPTIONS

`-inputs, -outputs`:  Insert a buffer between the input and load, output and load respectively. The default behavior is `-inputs` and `-outputs` set if neither is specified.

`-max_utilization`:  Defines the percentage of core area used.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
