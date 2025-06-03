---
title: set_dft_config(2)
date: 24/09/08
---

# NAME

set_dft_config - set dft config

# SYNOPSIS

set_dft_config 
    [-max_length <int>]
    [-max_chains <int>]
    [-clock_mixing <string>]


# DESCRIPTION

The command `set_dft_config` sets the DFT configuration variables.

# OPTIONS

`-max_length`:  The maximum number of bits that can be in each scan chain.

`-max_chains`: 

`-clock_mixing`:  How architect will mix the scan flops based on the clock driver. `no_mix`: Creates scan chains with only one type of clock and edge. This may create unbalanced chains. `clock_mix`: Creates scan chains mixing clocks and edges. Falling edge flops are going to be stitched before rising edge.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
