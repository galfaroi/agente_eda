---
title: clock_tree_synthesis(2)
date: 24/09/08
---

# NAME

clock_tree_synthesis - clock tree synthesis

# SYNOPSIS

clock_tree_synthesis 
    [-wire_unit wire_unit]
    [-buf_list <list_of_buffers>]
    [-root_buf root_buf]
    [-clk_nets <list_of_clk_nets>]
    [-tree_buf <buf>]
    [-distance_between_buffers]
    [-branching_point_buffers_distance]
    [-clustering_exponent]
    [-clustering_unbalance_ratio]
    [-sink_clustering_size cluster_size]
    [-sink_clustering_max_diameter max_diameter]
    [-sink_clustering_enable]
    [-balance_levels]
    [-sink_clustering_levels levels]
    [-num_static_layers]
    [-sink_clustering_buffer]
    [-obstruction_aware]
    [-apply_ndr]
    [-insertion_delay]
    [-dont_use_dummy_load]
    [-sink_buffer_max_cap_derate derate_value]
    [-delay_buffer_derate derate_value]


# DESCRIPTION

Perform clock tree synthesis.

# OPTIONS

`-buf_list`:  Tcl list of master cells (buffers) that will be considered when making the wire segments (e.g. `{BUFXX, BUFYY}`).

`-root_buffer`:  The master cell of the buffer that serves as root for the clock tree. If this parameter is omitted, the first master cell from `-buf_list` is taken.

`-wire_unit`:  Minimum unit distance between buffers for a specific wire. If this parameter is omitted, the code gets the value from ten times the height of `-root_buffer`.

`-distance_between_buffers`:  Distance (in microns) between buffers that `cts` should use when creating the tree. When using this parameter, the clock tree algorithm is simplified and only uses a fraction of the segments from the LUT.

`-branching_point_buffers_distance`:  Distance (in microns) that a branch has to have in order for a buffer to be inserted on a branch end-point. This requires the `-distance_between_buffers` value to be set.

`-clustering_exponent`:  Value that determines the power used on the difference between sink and means on the CKMeans clustering algorithm. The default value is `4`, and the allowed values are integers `[0, MAX_INT]`.

`-clustering_unbalance_ratio`:  Value determines each cluster's maximum capacity during CKMeans. A value of `0.5` (i.e., 50%) means that each cluster will have exactly half of all sinks for a specific region (half for each branch). The default value is `0.6`, and the allowed values are floats `[0, 1.0]`.

`-sink_clustering_enable`:  Enables pre-clustering of sinks to create one level of sub-tree before building H-tree. Each cluster is driven by buffer which becomes end point of H-tree structure.

`-sink_clustering_size`:  Specifies the maximum number of sinks per cluster. The default value is `20`, and the allowed values are integers `[0, MAX_INT]`.

`-sink_clustering_max_diameter`:  Specifies maximum diameter (in microns) of sink cluster. The default value is `50`, and the allowed values are integers `[0, MAX_INT]`.

`-balance_levels`:  Attempt to keep a similar number of levels in the clock tree across non-register cells (e.g., clock-gate or inverter). The default value is `False`, and the allowed values are bool.

`-clk_nets`:  String containing the names of the clock roots. If this parameter is omitted, `cts` looks for the clock roots automatically.

`-num_static_layers`:  Set the number of static layers. The default value is `0`, and the allowed values are integers `[0, MAX_INT]`.

`-sink_clustering_buffer`:  Set the sink clustering buffer(s) to be used.

`-obstruction_aware`:  Enables obstruction-aware buffering such that clock buffers are not placed on top of blockages or hard macros. This option may reduce legalizer displacement, leading to better latency, skew or timing QoR.  The default value is `False`, and the allowed values are bool.

`-apply_ndr`:  Applies 2X spacing non-default rule to all clock nets except leaf-level nets. The default value is `False`.

`-dont_use_dummy_load`:  Don't apply dummy buffer or inverter cells at clock tree leaves to balance loads. The default values is `False`.

`-sink_buffer_max_cap_derate`:  Use this option to control automatic buffer selection. To favor strong(weak) drive strength buffers use a small(large) value.  The default value is `0.01`, meaning that buffers are selected by derating max cap limit by 0.01. The value of 1.0 means no derating of max cap limit. 

`-delay_buffer_derate`:  This option balances latencies between macro cells and registers by inserting delay buffers.  The default value is `1.0`, meaning all needed delay buffers are inserted.  A value of 0.5 means only half of necessary delay buffers are inserted.  A value of 0.0 means no insertion of delay buffers.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
