---
title: set_dont_use(2)
date: 24/09/08
---

# NAME

set_dont_use - set dont use

# SYNOPSIS

set_dont_use lib_cells 


# DESCRIPTION

The `set_dont_use` command removes library cells from consideration by
the `resizer` engine and the `CTS` engine. `lib_cells` is a list of cells returned by `get_lib_cells`
or a list of cell names (`wildcards` allowed). For example, `DLY*` says do
not use cells with names that begin with `DLY` in all libraries.

# OPTIONS

This command has no switches.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
