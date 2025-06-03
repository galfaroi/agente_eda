---
title: create_power_switch(2)
date: 24/09/08
---

# NAME

create_power_switch - create power switch

# SYNOPSIS

create_power_switch
    [-domain domain]
    [-output_supply_port output_supply_port]
    [-input_supply_port input_supply_port]
    [-control_port control_port]
    [-on_state on_state]
    name


# DESCRIPTION

This command creates power switch.

# OPTIONS

`-domain`:  Power domain name.

`-output_supply_port`:  Output supply port of the switch.

`-input_supply_port`:  Input supply port of the switch.

`-control_port`:  Control port on the switch.

`-on_state`:  One of {`state_name`, `input_supply_port`, `boolean_expression`}.

`name`:  Power switch name.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
