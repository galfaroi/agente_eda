---
title: bench_wires(2)
date: 24/09/08
---

# NAME

bench_wires - bench wires

# SYNOPSIS

bench_wires
    [-met_cnt mcnt]
    [-cnt count]
    [-len wire_len]
    [-over]
    [-diag]
    [-all]
    [-db_only]
    [-under_met layer]
    [-w_list width]
    [-s_list space]
    [-over_dist dist]
    [-under_dist dist]


# DESCRIPTION

The `bench_wires` command produces a layout which contains various patterns
that are used to characterize per-unit length R and C values. The generated patterns model
the lateral, vertical, and diagonal coupling capacitances, as well as ground
capacitance effects. This command generates a .def file that contains a number of wire patterns.

This command is specifically intended for the Extraction Rules file generation only.

# OPTIONS

`-met_cnt`:  Number of layers used in each pattern. The default value is `-1`, meaning it is not set, and the allowed values are integers `[0, MAX_INT]`.

`-cnt`:  Number of wires in each pattern. The default value is `5`, and the default values are integers `[0, MAX_INT]`.

`-len`:  Wirelength in microns in the pattern. The default value is `100`, and the allowed values are integers `[0, MAX_INT]`.

`-all`:  Consider all different pattern geometries (`over`, `under`, `over_under`, and `diagonal`).

`-db_only`:  Run with db values only. All parameters in `bench_wires` are ignored.

`-under_met`:  Consider under metal layer.

`-w_list`:  Lists of wire width multipliers from the minimum spacing defined in the LEF.

`-s_list`:  Lists of wire spacing multipliers from the minimum spacing defined in the LEF. The list will be the input index on the OpenRCX RC table (Extraction Rules file).

`-over_dist, -under_dist`:  Consider over and under metal distance respectively.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
