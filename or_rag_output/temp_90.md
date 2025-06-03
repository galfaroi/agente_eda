---
title: create_toolbar_button(2)
date: 24/09/08
---

# NAME

create_toolbar_button - create toolbar button

# SYNOPSIS

create_toolbar_button 
    [-name name]
    -text button_text
    -script tcl_script 
    [-echo]


# DESCRIPTION

This command creates toolbar button with name set using the
`-text` flag and accompanying logic in the `-script` flag.

Returns: name of the new button, either ``name`` or ``buttonX``.

# OPTIONS

`-name`:  The name of the button, used when deleting the button.

`-text`:  The text to put on the button.

`-script`:  The tcl script to evaluate when the button is pressed.

`-echo`:  This indicate that the commands in the ``tcl_script`` should be echoed in the log.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
