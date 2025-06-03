---
title: global_placement_debug(2)
date: 24/09/08
---

# NAME

global_placement_debug - global placement debug

# SYNOPSIS

global_placement_debug
    [-pause] 
    [-update]
    [-inst]
    [-draw_bins]
    [-initial]


# DESCRIPTION

The `global_placement_debug` command initiates a debug mode, enabling real-time visualization of the algorithm's progress on the layout. Use the command prior to executing the `global_placement` command, for example in the `global_place.tcl` script.

# OPTIONS

`-pause`:  Number of iterations between pauses during debugging. Allows for visualization of the current state. Useful for closely monitoring the progression of the placement algorithm. Allowed values are integers, default is 10.

`-update`:  Defines the frequency (in iterations) at which the tool refreshes its layout output to display the latest state during debugging. Allowed values are integers, default is 10. 

`-inst`:  Targets a specific instance name for debugging focus. Allowed value is a string, the default behavior focuses on no specific instance.

`-draw_bins`:  Activates visualization of placement bins, showcasing their density (indicated by the shade of white) and the direction of forces acting on them (depicted in red). The default setting is disabled.

`-initial`:  Pauses the debug process during the initial placement phase. The default setting is disabled.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
