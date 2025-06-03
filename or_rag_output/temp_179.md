---
title: make_fake_io_site(2)
date: 24/09/08
---

# NAME

make_fake_io_site - make fake io site

# SYNOPSIS

make_fake_io_site 
    -name name
    -width width
    -height height


# DESCRIPTION

If the library does not contain sites for the IO cells, the following command can be used to add them.
This should not be used unless the sites are not in the library.

Example usage:

```
make_fake_io_site -name IO_HSITE -width 1 -height 204
make_fake_io_site -name IO_VSITE -width 1 -height 200
make_fake_io_site -name IO_CSITE -width 200 -height 204
```

# OPTIONS

`-name`:  Name of the site.

`-width`:  Width of the site (in microns).

`-height`:  Height of the site (in microns).

# ARGUMENTS

This command has no arguments.

# EXAMPLES

# SEE ALSO
