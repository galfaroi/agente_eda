---
title: tapcell(2)
date: 24/09/08
---

# NAME

tapcell - tapcell

# SYNOPSIS

tapcell 
    [-tapcell_master tapcell_master]
    [-tap_prefix tap_prefix]
    [-endcap_master endcap_master]
    [-endcap_prefix endcap_prefix]
    [-distance dist]
    [-disallow_one_site_gaps]
    [-halo_width_x halo_x]
    [-halo_width_y halo_y]
    [-tap_nwin2_master tap_nwin2_master]
    [-tap_nwin3_master tap_nwin3_master]
    [-tap_nwout2_master tap_nwout2_master]
    [-tap_nwout3_master tap_nwout3_master]
    [-tap_nwintie_master tap_nwintie_master]
    [-tap_nwouttie_master tap_nwouttie_master]
    [-cnrcap_nwin_master cnrcap_nwin_master]
    [-cnrcap_nwout_master cnrcap_nwout_master]
    [-incnrcap_nwin_master incnrcap_nwin_master]
    [-incnrcap_nwout_master incnrcap_nwout_master]
    [-tbtie_cpp tbtie_cpp]
    [-endcap_cpp endcap_cpp]
    [-no_cell_at_top_bottom]


# DESCRIPTION

This command inserts tapcells or endcaps.

The figures below show two examples of tapcell insertion. When only the 
`-tapcell_master` and `-endcap_master` masters are given, the tapcell placement
is similar to Figure 1. When the remaining masters are give, the tapcell
placement is similar to Figure 2.

| <img src="./doc/image/tapcell_example1.svg" width=450px> | <img src="./doc/image/tapcell_example2.svg" width=450px> |
|:--:|:--:|
| Figure 1: Tapcell insertion representation | Figure 2:  Tapcell insertion around macro representation |

# OPTIONS

`-tapcell_master`:  Master used as a tapcell.

`-tap_prefix`:  Prefix for the tapcell instances. The default value is `TAP_`.

`-endcap_master`:  Master used as an endcap.

`-endcap_prefix`:  Prefix for the endcaps instances. The default value is `PHY_`.

`-distance`:  Distance (in microns) between each tapcell in the checkerboard.

`-disallow_one_site_gaps`:  KIV.

`-halo_width_x`:  Horizontal halo size (in microns) around macros during cut rows.

`-halo_width_y`:  Vertical halo size (in microns) around macros during cut rows.

`-tap_nwintie_master`:  Master cell placed at the top and bottom of|macros and the core area according the row orientation.

`-tap_nwin2_master`:  Master cell placed at the top and bottom of macros and the core area according the row orientation. This master should be smaller than `tap_nwintie_master`

`-tap_nwin3_master`:  Master cell placed at the top and bottom of macros and the core area according the row orientation. This master should be smaller than `tap_nwin2_master`.

`-tap_nwouttie_master`:  Master cell placed at the top and bottom of macros and the core area according the row orientation.

`-tap_nwout2_master`:  Master cell placed at the top and bottom of macros and the core area according the row orientation. This master should be smaller than `tap_nwouttie_master`.

`-tap_nwout3_master`:  Master cell placed at the top and bottom of macros and the core area according the row orientation | This master should be smaller than `tap_nwout2_master`.

`-incnrcap_nwin_master`:  Master cell placed at the corners of macros, according the row orientation.

`-incnrcap_nwout_master`:  Master cell placed at the corners of macros, according the row orientation.

`-cnrcap_nwin_master`:  Macro cell placed at the corners the core area according the row orientation.

`-cnrcap_nwout_master`:  Macro cell placed at the corners the core area according the row orientation.

`-tbtie_cpp`:  Option is deprecated.

`-endcap_cpp`:  Option is deprecated.

`-no_cell_at_top_bottom`:  Option is deprecated.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
