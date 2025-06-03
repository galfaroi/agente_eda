---
title: diff_spef(2)
date: 24/09/08
---

# NAME

diff_spef - diff spef

# SYNOPSIS

diff_spef
    [-file filename]                
    [-r_res]
    [-r_cap]
    [-r_cc_cap]
    [-r_conn]


# DESCRIPTION

The `diff_spef` command compares the parasitics in the reference database `<filename>.spef`.
The output of this command is `diff_spef.out`
and contains the RC numbers from the parasitics in the database and the
`<filename>.spef`, and the percentage RC difference of the two data.

# OPTIONS

`-file`:  Path to the input `.spef` filename.

`-r_res`:  Read resistance.

`-r_cap`:  Read capacitance.

`-r_cc_cap`:  Read coupled capacitance.

`r_conn`:  Read connections.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
