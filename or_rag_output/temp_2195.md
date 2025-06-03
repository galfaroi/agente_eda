---
title: extract_parasitics(2)
date: 24/09/08
---

# NAME

extract_parasitics - extract parasitics

# SYNOPSIS

extract_parasitics
    [-ext_model_file filename]      
    [-corner_cnt count]            
    [-max_res ohms]               
    [-coupling_threshold fF]        
    [-debug_net_id id]
    [-lef_res]                     
    [-cc_model track]             
    [-context_depth depth]      
    [-no_merge_via_res]       


# DESCRIPTION

The `extract_parasitics` command performs parasitic extraction based on the
routed design. If there are no information on routed design, no parasitics are
returned.

# OPTIONS

`-ext_model_file`:  Specify the Extraction Rules file used for the extraction.

`-corner_cnt`:  Defines the number of corners used during the parasitic extraction.

`-max_res`:  Combines resistors in series up to the threshold value.

`-coupling_threshold`:  Coupling below this threshold is grounded. The default value is `0.1`, units are in `fF`, accepted values are floats.

`-debug_net_id`:  *Developer Option*: Net ID to evaluate.

`-lef_res`:  Override LEF resistance per unit.

`-cc_model`:  Specify the maximum number of tracks of lateral context that the tool considers on the same routing level. The default value is `10`, and the allowed values are integers `[0, MAX_INT]`.

`-context_depth`:  Specify the number of levels of vertical context that OpenRCX needs to consider for the over/under context overlap for capacitance calculation. The default value is `5`, and the allowed values are integers `[0, MAX_INT]`.

`-no_merge_via_res`:  Separates the via resistance from the wire resistance.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
