---
title: bench_verilog(2)
date: 24/09/08
---

# NAME

bench_verilog - bench verilog

# SYNOPSIS

bench_verilog
    [filename]                    


# DESCRIPTION

`bench_verilog` is used after the `bench_wires` command. This command
generates a Verilog netlist of the generated pattern layout by the `bench_wires`
command.

This command is optional when running the Extraction Rules generation
flow. This step is required if the favorite extraction tool (i.e., reference
extractor) requires a Verilog netlist to extract parasitics of the pattern layout.

# OPTIONS

`filename`:  Name for the Verilog output file (e.g., `output.v`).

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
