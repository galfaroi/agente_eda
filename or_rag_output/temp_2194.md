---
title: set_wire_rc(2)
date: 24/09/08
---

# NAME

set_wire_rc - set wire rc

# SYNOPSIS

set_wire_rc 
    [-clock] 
    [-signal]
    [-data]
    [-corner corner]
    [-layers layers_list]

or 
set_wire_rc
    [-h_resistance res]
    [-h_capacitance cap]
    [-v_resistance res]
    [-v_capacitance cap]

or
set_wire_rc 
    [-clock] 
    [-signal]
    [-data]
    [-corner corner]
    [-layer layer_name]
or 
set_wire_rc
    [-resistance res]
    [-capacitance cap]


# DESCRIPTION

The `set_wire_rc` command sets the resistance and capacitance used to estimate
delay of routing wires.  Separate values can be specified for clock and data
nets with the `-signal` and `-clock` flags. Without either `-signal` or
`-clock` the resistance and capacitance for clocks and data nets are set.

```
# Either run 
set_wire_rc -clock ... -signal ... -layer ...

# Or
set_wire_rc -resistance ... -capacitance ...
```

# OPTIONS

`-clock`:  Enable setting of RC for clock nets.

`-signal`:  Enable setting of RC for signal nets.

`-layers`:  Use the LEF technology resistance and area/edge capacitance values for the layers. The values for each layers will be used for wires with the prefered layer direction, if 2 or more layers have the same prefered direction the avarege value is used for wires with that direction. This is used for a default width wire on the layer.

`-layer`:  Use the LEF technology resistance and area/edge capacitance values for the layer. This is used for a default width wire on the layer.

`-resistance`:  Resistance per unit length, units are from the first Liberty file read.

`-capacitance`:  Capacitance per unit length, units are from the first Liberty file read.

`-h_resistance`:  Resistance per unit length for horizontal wires, units are from the first Liberty file read.

`-h_capacitance`:  Capacitance per unit length for horizontal wires, units are from the first Liberty file read.

`-v_resistance`:  Resistance per unit length for vertical wires, units are from the first Liberty file read.

`-v_capacitance`:  Capacitance per unit length for vertical wires, units are from the first Liberty file read.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
