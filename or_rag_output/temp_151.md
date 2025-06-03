---
title: remove_buffers(2)
date: 24/09/08
---

# NAME

remove_buffers - remove buffers

# SYNOPSIS

remove_buffers
    [ instances ]


# DESCRIPTION

Use the `remove_buffers` command to remove buffers inserted by synthesis. This
step is recommended before using `repair_design` so that there is more flexibility
in buffering nets.  If buffer instances are specified, only specified buffer instances
will be removed regardless of dont-touch or fixed cell.  Direct input port to output port
feedthrough buffers will not be removed.
If no buffer instances are specified, all buffers will be removed except those that are associated with
dont-touch, fixed cell or direct input port to output port feedthrough buffering.

# OPTIONS

This command has no switches.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
