M2R
===

[![PyPI](https://img.shields.io/pypi/v/m2r.svg)](https://pypi.python.org/pypi/m2r)
[![PyPI version](https://img.shields.io/pypi/pyversions/m2r.svg)](https://pypi.python.org/pypi/m2r)
[![Build Status](https://travis-ci.org/miyakogi/m2r.svg?branch=master)](https://travis-ci.org/miyakogi/m2r)
[![codecov](https://codecov.io/gh/miyakogi/m2r/branch/master/graph/badge.svg)](https://codecov.io/gh/miyakogi/m2r)

--------------------------------------------------------------------------------

M2R converts a markdown file including reST markups to a valid reST format.

## Why another converter?

I wanted to write sphinx document in markdown, since it's widely used now and
easy to write code blocks and lists. However, converters using pandoc or
recommonmark do not support many reST markups and sphinx extensions. For
example, reST's reference link like ``see `ref`_`` (this is very convenient in
long document in which same link appears multiple times) will be converted to
a code block in HTML like `see <code>ref</code>_`, which is not expected.

## Features

* Basic markdown and some extensions (see below)
    * inline/block-level raw html
    * fenced-code block
    * tables
    * footnotes (``[^1]``)
* Inline- and Block-level reST markups
    * single- and multi-line directives (`.. directive::`)
    * inline-roles (``:code:`print(1)` ...``)
    * ref-link (``see `ref`_``)
    * footnotes (``[#fn]_``)
    * math extension inspired by [recommonmark](https://recommonmark.readthedocs.io/en/latest/index.html)
* Sphinx extension
    * add markdown support for sphinx
    * ``mdinclude`` directive to include markdown from md or reST files

## Installation

Python 2.7 or Python 3.3+ is required.

```
pip install m2r
```

## Usage

### Command Line

`m2r` command converts markdown file to reST format.

```
m2r your_document.md [your_document2.md ...]
```

Then you will find `your_document.rst` in the same directory.

### Programmatic Use

Instantiate `M2R` class and call with markdown text. Then it will return converted text.

```python
from m2r import M2R
m2r = M2R()
rest = m2r('# Title\n\nSentence.')
print(rest)
# Title
# =====
#
# Sentence.
```

Or, use `parse_from_file` function to load markdown file and obtain converted text.

```python
from m2r import parse_from_file
output = parse_from_file('markdown_file.md')
```

This is an example of setup.py to write README in markdown, and publish it to PyPI as reST format.

```python
readme_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md')
try:
    from m2r import parse_from_file
    readme = parse_from_file(readme_file)
except ImportError:
    # m2r may not be installed in user environment
    with open(readme_file) as f:
        readme = f.read()
setup(
    ...,
    long_description=readme,
    ...,
)
```

### Sphinx Integration

In your conf.py, add the following lines.

```python
extensions = [
    ...,
    'm2r',
]

# source_suffix = '.rst'
source_suffix = ['.rst', '.md']
```

Write index.md and run `make html`.

When `m2r` extension is enabled on sphinx and `.md` file is loaded, m2r
converts to reST and pass to sphinx, not making new `.rst` file.

#### mdinclude directive

Like `.. include:: file` directive, `.. mdinclude:: file` directive inserts
markdown file at the line.

Note: do not use `.. include:: file` directive to include markdown file even if
in the markdown file, please use `.. mdinclude:: file` instead.

## Restrictions

* In the reST's directives, markdown is not available. Please write in reST.
* Column alignment of tables is not supported. (reST does not support this feature)
* Heading with overline-and-underline is not supported.
  * Heading with underline is OK

If you find any bug or unexpected behaviour, please report it to
[Issues](https://github.com/miyakogi/m2r/issues).

## Example

See [example document](https://miyakogi.github.io/m2r/example.html) and [its
source code](https://github.com/miyakogi/m2r/blob/master/docs/example.md).

I'm using m2r for writing user guide of [WDOM](https://github.com/miyakogi/wdom).
So you can see it as another example. Its [HTML is
here](http://wdom-py.readthedocs.io/en/latest/guide/index.html), and [its
source code is here](https://github.com/miyakogi/wdom/tree/dev/docs/guide).

## Acknowledgement

m2r is written as an extension of
[mistune](http://mistune.readthedocs.io/en/latest/), which is highly extensible
pure-python markdown parser.
Without the mistune, I couldn't write this. Thank you!

## Licence

[MIT](https://github.com/miyakogi/m2r/blob/master/LICENSE)
