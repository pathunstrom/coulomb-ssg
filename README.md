# Coulomb

A new static site generator.

Inspired by [statik]'s strong points:

* Customizable data model
* Data is markdown files on disk
* Views are mostly declarative configuration

Created due to some of its weak points:

* YAML configuration means bad configs give unhelpful errors
* Outside underlying technology, has very few opinions.
* No batteries included.
* SQLAlchemy queries embedded in YAML sucks.

## Goals

The goal of coulomb is to have the same level of power and flexibility as
statik but with the burrs removed and a much nicer onboarding experience.

### Configuration

Python is a great configuration language! It's strongly typed, so you get
proper type errors, and your linting tools know what you're doing. It also
opens up your configuration to the same kind of tools you use to write
software.

### Batteries Included

Certain types of views should be bundled with the tool:

* blogs
* portfolios
* serial posts
* pages

All of these should work out of the box, and provide ready to use data models.
That said, they should be fully optional and extending or replacing them
should be valid.

### Helpful Errors

If you messed up a view configuration or query in statik, you'd often get an
opaque error from the yaml decoding library or SQL alchemy, and often at build
time. Coulomb should allow as much as possible to be checked via static
analysis tools and a validation routine that can target specific models and
views to provide ahead of build failure warnings.

### Onboarding

Coulomb should have a cookie cutter or similar tool for generating a working
configuration. It should make it very easy to add new configurations to
existing projects. The shape of your files should also be configurable.

[statik]: https://getstatik.com/