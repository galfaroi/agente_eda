---
title: insert_tiecells(2)
date: 24/09/08
---

# NAME

insert_tiecells - insert tiecells

# SYNOPSIS

insert_tiecells 
    tie_pin
    [-prefix inst_prefix]


# DESCRIPTION

This comamnd inserts tiecells.

# OPTIONS

`tie_pin`:  Indicates the master and port to use to tie off nets. For example, `LOGIC0_X1/Z` for the Nangate45 library, where `LOGIC0_X1` is the master and `Z` is the output port on the master.

`-prefix`:  Used to control the prefix of the new tiecell names. This will default to `TIEOFF_`.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
