---
title: man(2)
date: 24/09/08
---

# NAME

man - man

# SYNOPSIS

man
    name
    [-manpath manpath]
    [-no_pager]


# DESCRIPTION

The `man` command in OpenROAD is similar in functionality to Unix
(and Unix-like operating systems such as Linux) . It is used to 
display the manual pages for various applications, tools and error 
messages. These manual pages provide detailed information about how
to use a particular command or function, along with its syntax and options.

This can be used for a range of commands in different levels as follows:
- Level 1: Top-level openroad command (e.g. `man openroad`)
- Level 2: Individual module commands (e.g. `man clock_tree_synthesis`)
- Level 3: Info, error, warning messages (e.g. `man CTS-0001`)

# OPTIONS

`name`:  Name of the command/message to query.

`-manpath`:  Include optional path to man pages (e.g. ~/OpenROAD/docs/cat).

`-no_pager`:  This flag determines whether you wish to see all of the man output at once. Default value is `False`, which shows a buffered output.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
