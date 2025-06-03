---
title: define_power_switch_cell(2)
date: 24/09/08
---

# NAME

define_power_switch_cell - define power switch cell

# SYNOPSIS

define_power_switch_cell 
    -name name 
    -control control_pin
    -power_switchable power_switchable_pin
    -power unswitched_power_pin
    -ground ground_pin 
    [-acknowledge acknowledge_pin_name]


# DESCRIPTION

Define a power switch cell that will be inserted into a power grid 

Example usage:

```
define_power_switch_cell -name POWER_SWITCH -control SLEEP -switched_power VDD -power VDDG -ground VSS
```

# OPTIONS

`-name`:  The name of the power switch cell.

`-control`:  The name of the power control port of the power switch cell.

`-switched_power`:  Defines the name of the pin that outputs the switched power net.

`-power`:  Defines the name of the pin that connects to the unswitched power net.

`-ground`:  Defines the name of the pin that connects to the ground net.

`-acknowledge`:  Defines the name of the output control signal of the power control switch if it has one.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
