---
title: define_pdn_grid(2)
date: 24/09/08
---

# NAME

define_pdn_grid - define pdn grid

# SYNOPSIS

define_pdn_grid 
    [-name name] 
    [-macro]
    [-existing]
    [-voltage_domains list_of_domain_names] 
    [-grid_over_pg_pins|-grid_over_boundary]
    [-orient list_of_valid_orientations]
    [-instances list_of_instances]
    [-cells list_of_cells]
    [-default]
    [-halo list_of_halo_values]
    [-pins list_of_pin_layers] 
    [-starts_with POWER|GROUND] 
    [-obstructions list_of_layers]
    [-power_switch_cell name]
    [-power_control signal_name]
    [-power_control_network STAR|DAISY]


# DESCRIPTION

```{warning}
`define_pdn_grid` is overloaded with two different signatures. Take note of the arguments when using this function!
```

- Method 1: General Usage
Define the rules to describe a power grid pattern to be placed in the design.

Example usage:

```
define_pdn_grid -name main_grid -pins {metal7} -voltage_domain {CORE TEMP_ANALOG}
```

- Method 2: Macros
Define the rules for one or more macros.

Example usage:

```
define_pdn_grid -macro -name ram          -orient {R0 R180 MX MY} -grid_over_pg_pins  -starts_with POWER -pin_direction vertical
define_pdn_grid -macro -name rotated_rams -orient {E FE W FW}     -grid_over_boundary -starts_with POWER -pin_direction horizontal
```

- Method 3: Modify existing power domain
Modify pre-existing power domain.

Example usage:

```
define_pdn_grid -name main_grid -existing
```

# OPTIONS

`-name`:  Defines a name to use when referring to this grid definition.

`-voltage_domains`:  Defines the name of the voltage domain for this grid (Default: Last domain created).

`-pins`:  Defines a list of layers which where the power straps will be promoted to block pins.

`-starts_with`:  Specifies whether the first strap placed will be POWER or GROUND (Default: GROUND).

`-obstructions`:  Specify the layers to add routing blockages, in order to avoid DRC violations.

`-macro`:  Defines the type of grid being added as a macro.

`-grid_over_pg_pins, -grid_over_boundary`:  Place the power grid over the power ground pins of the macro. (Default True), or Place the power grid over the entire macro. 

`-orient`:  For a macro, defines a set of valid orientations. LEF orientations (N, FN, S, FS, E, FE, W and FW) can be used as well as standard geometry orientations (R0, R90, R180, R270, MX, MY, MXR90 and MYR90). Macros with one of the valid orientations will use this grid specification.

`-instances`:  For a macro, defines a set of valid instances. Macros with a matching instance name will use this grid specification.

`-cells`:  For a macro, defines a set of valid cells. Macros which are instances of one of these cells will use this grid specification.

`-default`:  For a macro, specifies this is a default grid that can be overwritten.

`-halo`:  Specifies the default minimum separation of selected macros from other cells in the design. This is only used if the macro does not define halo values in the LEF description. If 1 value is specified it will be used on all 4 sides, if two values are specified, the first will be applied to left/right sides and the second will be applied to top/bottom sides, if 4 values are specified, then they are applied to left, bottom, right and top sides respectively (Default: 0).

`-power_switch_cell`:  Defines the name of the coarse grain power switch cell to be used wherever the stdcell rail connects to the rest of the power grid. The mesh layers are associated with the unswitched power net of the voltage domain, whereas the stdcell rail is associated with the switched power net of the voltage domain. The placement of a power switch cell connects the unswitched power mesh to the switched power rail through a power switch defined by the `define_power_switch_cell` command.

`-power_control`:  Defines the name of the power control signal used to control the switching of the inserted power switches.

`-power_control_network`:  Defines the structure of the power control signal network. Choose from STAR, or DAISY. If STAR is specified, then the network is wired as a high-fanout net with the power control signal driving the power control pin on every power switch. If DAISY is specified then the power switches are connected in a daisy-chain configuration - note, this requires that the power swich defined by the `define_power_switch_cell`  command defines an acknowledge pin for the switch.

`-existing`:  Flag to enable defining for existing routing solution.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
