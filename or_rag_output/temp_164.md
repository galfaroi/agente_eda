---
title: select(2)
date: 24/09/08
---

# NAME

select - select

# SYNOPSIS

select 
    -type object_type
    [-name glob_pattern]
    [-filter attribute=value]
    [-case_insensitive]
    [-highlight group]


# DESCRIPTION

This command selects object based on options.
Returns: number of objects selected.

# OPTIONS

`-type`:  name of the object type. For example, ``Inst`` for instances, ``Net`` for nets, and ``DRC`` for DRC violations

`-name`:  (optional) filter selection by the specified name. For example, to only select clk nets ``*clk*``. Use ``-case_insensitive`` to filter based on case insensitive instead of case sensitive

`-filter`:  (optional) filter selection based on the objects' properties. ``attribute`` represents the property's name and ``value`` the property's value. In case the property holds a collection (e. g. BTerms in a Net) or a table (e. g. Layers in a Generate Via Rule) ``value`` can be any element within those. A special case exists for checking whether a collection is empty or not by using the value ``CONNECTED``. This can be useful to select a specific group of elements (e. g. BTerms=CONNECTED will select only Nets connected to Input/Output Pins)

`-highlight`:  (optional) add the selection to the specific highlighting group. Values can be 0 to 7.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
