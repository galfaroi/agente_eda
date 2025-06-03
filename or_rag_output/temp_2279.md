---
title: write_rules(2)
date: 24/09/08
---

# NAME

write_rules - write rules

# SYNOPSIS

write_rules
  [-file filename]           
  [-dir dir]
  [-name name]
  [-pattern pattern]
  [-db]


# DESCRIPTION

The `write_rules` command writes the Extraction Rules file (RC technology file)
for OpenRCX. It processes the parasitics data from the layout patterns that are
generated using the `bench_wires` command, and writes the Extraction Rules file
with `<filename>` as the output file.

This command is specifically intended for the purpose of Extraction Rules file
generation.

# OPTIONS

`-file`:  Output file name.

`-dir`:  Output file directory.

`-name`:  Name of rule.

`-pattern`:  Flag to write the pattern to rulefile (0/1).

`-db`:  DB tbc.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
