---
title: set_pdnsim_source_settings(2)
date: 24/09/08
---

# NAME

set_pdnsim_source_settings - set pdnsim source settings

# SYNOPSIS

set_pdnsim_source_settings
    [-bump_dx pitch]
    [-bump_dy pitch]
    [-bump_size size]
    [-bump_interval interval]
    [-strap_track_pitch pitch]


# DESCRIPTION

Set PDNSim power source setting.

# OPTIONS

`-bump_dx,-bump_dy`:  Set the bump pitch to decide the voltage source location. The default bump pitch is 140um.

`-bump_size`:  Set the bump size. The default bump size is 70um.

`-bump_interval`:  Set the bump population interval, this is used to depopulate the bump grid to emulate signals and other power connections. The default bump pitch is 3.

`-strap_track_pitch`:  Sets the track pitck to use for moduling voltage sources as straps. The default is 10x.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
