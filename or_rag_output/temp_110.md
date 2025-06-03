---
title: set_voltage_domain(2)
date: 24/09/08
---

# NAME

set_voltage_domain - set voltage domain

# SYNOPSIS

set_voltage_domain 
    -name domain_name
    -power power_net_name 
    -ground ground_net_name
    [-region region_name]
    [-secondary_power secondary_power_net] 
    [-switched_power switched_power_net]


# DESCRIPTION

Defines a named voltage domain with the names of the power and ground nets for a region.

This region must already exist in the floorplan before referencing it with the `set_voltage_domain` command. If the `-region` argument is not supplied then region is the entire core area of the design.

Example usage:

```
set_voltage_domain -power VDD -ground VSS
set_voltage_domain -name TEMP_ANALOG -region TEMP_ANALOG -power VIN -ground VSS
set_voltage_domain -region test_domain -power VDD -ground VSS -secondary_power VREG
```

# OPTIONS

`-name`:  Defines the name of the voltage domain. The default is "Core" or region name if provided.

`-power`:  Specifies the name of the power net for this voltage domain.

`-ground`:  Specifies the name of the ground net for this voltage domain.

`-region`:  Specifies a region of the design occupied by this voltage domain.

`-secondary_power`:  Specifies the name of the secondary power net for this voltage domain.

`-switched_power`:  Specifies the name of the switched power net for switched power domains.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
