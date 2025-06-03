---
title: place_macro(2)
date: 24/09/08
---

# NAME

place_macro - place macro

# SYNOPSIS

place_macro
    -macro_name macro_name
    -location {x y}
    [-orientation orientation]


# DESCRIPTION

Command for manual placement of a single macro.

# OPTIONS

`-macro_name`:  The name of a macro of the design.

`-location`:  The lower left corner of the macro in microns.

`-orientation`:  The orientation according to odb. If nothing is specified, defaults to `R0`.  We only allow `R0`, `MY`, `MX` and `R180`. 

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
