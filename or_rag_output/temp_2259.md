---
title: repair_timing(2)
date: 24/09/08
---

# NAME

repair_timing - repair timing

# SYNOPSIS

repair_timing 
    [-setup]
    [-hold]
    [-recover_power percent_of_paths_with_slack]
    [-setup_margin setup_margin]
    [-hold_margin hold_margin]
    [-slack_margin slack_margin]
    [-libraries libs]
    [-allow_setup_violations]
    [-skip_pin_swap]
    [-skip_gate_cloning]
    [-skip_buffering]
    [-enable_buffer_removal]
    [-repair_tns tns_end_percent]
    [-max_passes passes]
    [-max_utilization util]
    [-max_buffer_percent buffer_percent]
    [-verbose]


# DESCRIPTION

The `repair_timing` command repairs setup and hold violations.  It
should be run after clock tree synthesis with propagated clocks.
Setup repair is done before hold repair so that hold repair does not
cause setup checks to fail.

The worst setup path is always repaired.  Next, violating paths to
endpoints are repaired to reduced the total negative slack.

# OPTIONS

`-setup`:  Repair setup timing.

`-hold`:  Repair hold timing.

`-recover_power`:  Set the percentage of paths to recover power for. The default value is `0`, and the allowed values are floats `(0, 100]`.

`-setup_margin`:  Add additional setup slack margin.

`-hold_margin`:  Add additional hold slack margin.

`-allow_setup_violations`:  While repairing hold violations, buffers are not inserted that will cause setup violations unless `-allow_setup_violations` is specified.

`-skip_pin_swap`:  Flag to skip pin swap. The default value is `False`, and the allowed values are bools.

`-skip_gate_cloning`:  Flag to skip gate cloning. The default value is `False`, and the allowed values are bools.

`-skip_buffering`:  Flag to skip rebuffering and load splitting. The default value is `False`, and the allowed values are bools.

`-enable_buffer_removal`:  Flag to enable buffer removal during setup fixing. The default value is `False`, and the allowed values are bools.

`-repair_tns`:  Percentage of violating endpoints to repair (0-100). When `tns_end_percent` is zero, only the worst endpoint is repaired. When `tns_end_percent` is 100 (default), all violating endpoints are repaired.

`-max_utilization`:  Defines the percentage of core area used.

`-max_buffer_percent`:  Specify a maximum number of buffers to insert to repair hold violations as a percentage of the number of instances in the design. The default value is `20`, and the allowed values are integers `[0, 100]`.

`-verbose`:  Enable verbose logging of the repair progress.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
