---
title: preview_dft(2)
date: 24/09/08
---

# NAME

preview_dft - preview dft

# SYNOPSIS

preview_dft
    [-verbose]


# DESCRIPTION

Prints a preview of the scan chains that will be stitched by `insert_dft`. Use
this command to iterate and try different DFT configurations. This command does
not perform any modification to the design, and should be run after `scan_replace`
and global placement.

# OPTIONS

`-verbose`:  Shows more information about each one of the scan chains that will be created.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
