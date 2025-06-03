---
title: restructure(2)
date: 24/09/08
---

# NAME

restructure - restructure

# SYNOPSIS

restructure 
    [-slack_threshold slack_val]
    [-depth_threshold depth_threshold]
    [-target area|delay]
    [-abc_logfile logfile]
    [-liberty_file liberty_file]
    [-tielo_port  tielo_pin_name]
    [-tiehi_port tiehi_pin_name]
    [-work_dir work_dir]


# DESCRIPTION

Restructuring can be done in two modes: area or delay.

- Method 1: Area Mode
Example: `restructure -liberty_file ckt.lib -target area -tielo_pin ABC -tiehi_pin DEF`

- Method 2: Timing Mode
Example: `restructure -liberty_file ckt.lib -target delay -tielo_pin ABC -tiehi_pin DEF -slack_threshold 1 -depth_threshold 2`

# OPTIONS

`-liberty_file`:  Liberty file with description of cells used in design. This is passed to ABC.

`-target`:  Either `area` or `delay`. In area mode, the focus is area reduction, and timing may degrade. In delay mode, delay is likely reduced, but the area may increase. The default value is `area`.

`-slack_threshold`:  Specifies a (setup) timing slack value below which timing paths need to be analyzed for restructuring. The default value is `0`, and the allowed values are floats `[0, MAX_FLOAT]`.

`-depth_threshold`:  Specifies the path depth above which a timing path would be considered for restructuring. The default value is `16`, and the allowed values are `[0, MAX_INT]`.

`-abc_logfile`:  Output file to save abc logs to.

`-work_dir`:  Name of the working directory for temporary files. If not provided, `run` directory would be used.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
