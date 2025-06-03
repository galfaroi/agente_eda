---
title: global_placement(2)
date: 24/09/08
---

# NAME

global_placement - global placement

# SYNOPSIS

global_placement
    [-timing_driven]
    [-routability_driven]
    [-disable_timing_driven]
    [-disable_routability_driven]
    [-skip_initial_place]
    [-incremental]
    [-bin_grid_count grid_count]
    [-density target_density]
    [-init_density_penalty init_density_penalty]
    [-init_wirelength_coef init_wirelength_coef]
    [-min_phi_coef min_phi_conef]
    [-max_phi_coef max_phi_coef]
    [-reference_hpwl reference_hpwl]
    [-overflow overflow]
    [-initial_place_max_iter initial_place_max_iter]
    [-initial_place_max_fanout initial_place_max_fanout]
    [-pad_left pad_left]
    [-pad_right pad_right]
    [-skip_io]
    [-skip_nesterov_place]
    [-routability_use_grt]
    [-routability_target_rc_metric routability_target_rc_metric]
    [-routability_check_overflow routability_check_overflow]
    [-routability_max_density routability_max_density]
    [-routability_max_bloat_iter routability_max_bloat_iter]
    [-routability_max_inflation_iter routability_max_inflation_iter]    
    [-routability_inflation_ratio_coef routability_inflation_ratio_coef]
    [-routability_max_inflation_ratio routability_max_inflation_ratio]
    [-routability_rc_coefficients routability_rc_coefficients]
    [-timing_driven_net_reweight_overflow]
    [-timing_driven_net_weight_max]
    [-timing_driven_nets_percentage]


# DESCRIPTION

When using the `-timing_driven` flag, `gpl` does a virtual `repair_design` 
to find slacks and
weight nets with low slack. It adjusts the worst slacks (modified with 
`-timing_driven_nets_percentage`) using a multiplier (modified with 
`-timing_driven_net_weight_max`). The multiplier
is scaled from the full value for the worst slack, to 1.0 at the
`timing_driven_nets_percentage` point. Use the `set_wire_rc` command to set
resistance and capacitance of estimated wires used for timing. 

Timing-driven iterations are triggered based on a list of overflow threshold 
values. Each time the placer execution reaches these overflow values, the 
resizer is executed. This process can be costly in terms of runtime. The 
overflow values for recalculating weights can be modified with 
`-timing_driven_net_reweight_overflow`, you may use less overflow threshold 
values to decrease runtime, for example.

When the routability-driven option is enabled, each of its iterations will 
execute RUDY to provide an estimation of routing congestion. Congested tiles 
will have the area of their logic cells inflated to reduce routing congestion. 
The iterations will attempt to achieve the target RC (routing congestion) 
by comparing it to the final RC at each iteration. If the algorithm takes too 
long during routability-driven execution, consider raising the target RC value 
(`-routability_target_rc_metric`) to alleviate the constraints. The final RC 
value is calculated based on the weight coefficients. The algorithm will stop 
if the RC is not decreasing for three consecutive iterations.

Routability-driven arguments
- They begin with `-routability`.
- `-routability_target_rc_metric`, `-routability_check_overflow`, `-routability_max_density`, `-routability_max_bloat_iter`, `-routability_max_inflation_iter`, `-routability_inflation_ratio_coef`, `-routability_max_inflation_ratio`, `-routability_rc_coefficients`

Timing-driven arguments
- They begin with `-timing_driven`.
- `-timing_driven_net_reweight_overflow`, `-timing_driven_net_weight_max`, `-timing_driven_nets_percentage`

# OPTIONS

`-timing_driven`:  Enable timing-driven mode. See [link](#timing-driven-arguments) for timing-specific arguments.

`-routability_driven`:  Enable routability-driven mode. See [link](#routability-driven-arguments) for routability-specific arguments.

`-skip_initial_place`:  Skip the initial placement (Biconjugate gradient stabilized, or BiCGSTAB solving) before Nesterov placement. Initial placement improves HPWL by ~5% on large designs. Equivalent to `-initial_place_max_iter 0`.

`-incremental`:  Enable the incremental global placement. Users would need to tune other parameters (e.g., `init_density_penalty`) with pre-placed solutions.

`-bin_grid_count`:  Set bin grid's counts. The internal heuristic defines the default value. Allowed values are integers `[64,128,256,512,...]`.

`-density`:  Set target density. The default value is `0.7` (i.e., 70%). Allowed values are floats `[0, 1]`.

`-init_density_penalty`:  Set initial density penalty. The default value is `8e-5`. Allowed values are floats `[1e-6, 1e6]`.

`-init_wirelength_coef`:  Set initial wirelength coefficient. The default value is `0.25`. Allowed values are floats.

`-min_phi_coef`:  Set `pcof_min` ($\mu_k$ Lower Bound). The default value is `0.95`. Allowed values are floats `[0.95, 1.05]`.

`-max_phi_coef`:  Set `pcof_max` ($\mu_k$ Upper Bound). Default value is 1.05. Allowed values are `[1.00-1.20, float]`.

`-overflow`:  Set target overflow for termination condition. The default value is `0.1`. Allowed values are floats `[0, 1]`.

`-initial_place_max_iter`:  Set maximum iterations in the initial place. The default value is 20. Allowed values are integers `[0, MAX_INT]`.

`-initial_place_max_fanout`:  Set net escape condition in initial place when $fanout \geq initial\_place\_max\_fanout$. The default value is 200. Allowed values are integers `[1, MAX_INT]`.

`-pad_left`:  Set left padding in terms of number of sites. The default value is 0, and the allowed values are integers `[1, MAX_INT]`

`-pad_right`:  Set right padding in terms of number of sites. The default value is 0, and the allowed values are integers `[1, MAX_INT]`

`-skip_io`:  Flag to ignore the IO ports when computing wirelength during placement. The default value is False, allowed values are boolean.

# ARGUMENTS

`-routability_use_grt`:  Use this tag to execute routability using FastRoute from grt for routing congestion, which is more precise but has a high runtime cost. By default, routability mode uses RUDY, which is faster.

`-routability_target_rc_metric`:  Set target RC metric for routability mode. The algorithm will try to reach this RC value. The default value is `1.01`, and the allowed values are floats.

`-routability_check_overflow`:  Set overflow threshold for routability mode. The default value is `0.3`, and the allowed values are floats `[0, 1]`.

`-routability_max_density`:  Set density threshold for routability mode. The default value is `0.99`, and the allowed values are floats `[0, 1]`.

`-routability_max_bloat_iter`:  Set bloat iteration threshold for routability mode. The default value is `1`, and the allowed values are integers `[1, MAX_INT]`

`-routability_max_inflation_iter`:  Set inflation iteration threshold for routability mode. The default value is `4`, and the allowed values are integers `[1, MAX_INT]`.

`-routability_inflation_ratio_coef`:  Set inflation ratio coefficient for routability mode. The default value is `5`, and the allowed values are floats.

`-routability_max_inflation_ratio`:  Set inflation ratio threshold for routability mode to prevent overly aggressive adjustments. The default value is `8`, and the allowed values are floats.

`-routability_rc_coefficients`:  Set routability RC coefficients for calculating the final RC. They relate to the 0.5%, 1%, 2%, and 5% most congested tiles. It comes in the form of a Tcl List `{k1, k2, k3, k4}`. The default value for each coefficient is `{1.0, 1.0, 0.0, 0.0}` respectively, and the allowed values are floats.

`-timing_driven_net_reweight_overflow`:  Set overflow threshold for timing-driven net reweighting. Allowed value is a Tcl list of integers where each number is `[0, 100]`. Default values are [79, 64, 49, 29, 21, 15]

`-timing_driven_net_weight_max`:  Set the multiplier for the most timing-critical nets. The default value is `1.9`, and the allowed values are floats.

`-timing_driven_nets_percentage`:  Set the reweighted percentage of nets in timing-driven mode. The default value is 10. Allowed values are floats `[0, 100]`.

# EXAMPLES

# SEE ALSO
