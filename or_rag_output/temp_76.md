---
title: make_io_bump_array(2)
date: 24/09/08
---

# NAME

make_io_bump_array - make io bump array

# SYNOPSIS

make_io_bump_array 
    -bump master
    -origin {x y}
    -rows rows
    -columns columns
    -pitch {x y}
    [-prefix prefix]


# DESCRIPTION

This command defines a bump array.

Example usage:

```
make_io_bump_array -bump BUMP -origin "200 200" -rows 14 -columns 14 -pitch "200 200"
```

# OPTIONS

`-bump`:  Name of the bump master.

`-origin`:  Origin of the array.

`-rows`:  Number of rows to create.

`-columns`:  Number of columns to create.

`-pitch`:  Pitch of the array.

`-prefix`:  Name prefix for the bump array. The default value is `BUMP_`.

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
