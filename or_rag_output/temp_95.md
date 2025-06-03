---
title: filler_placement(2)
date: 24/09/08
---

# NAME

filler_placement - filler placement

# SYNOPSIS

filler_placement
    [-prefix prefix]
    filler_masters


# DESCRIPTION

The `filler_placement` command fills gaps between detail-placed instances
to connect the power and ground rails in the rows. `filler_masters` is a
list of master/macro names to use for filling the gaps. Wildcard matching
is supported, so `FILL*` will match, e.g., `FILLCELL_X1 FILLCELL_X16 FILLCELL_X2
FILLCELL_X32 FILLCELL_X4 FILLCELL_X8`.  To specify a different naming prefix
from `FILLER_` use `-prefix <new prefix>`.

# OPTIONS

`-prefix`:  Prefix to name the filler cells. The default value is `FILLER_`.

`filler_masters`:  Filler master cells.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
