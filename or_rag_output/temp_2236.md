---
title: report_cts(2)
date: 24/09/08
---

# NAME

report_cts - report cts

# SYNOPSIS

report_cts 
    [-out_file file]


# DESCRIPTION

This command is used to extract the following metrics after a successful `clock_tree_synthesis` run. 
- Number of Clock Roots
- Number of Buffers Inserted
- Number of Clock Subnets
- Number of Sinks.

# OPTIONS

`-out_file`:  The file to save `cts` reports. If this parameter is omitted, the report is streamed to `stdout` and not saved.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
