M2R
===

[![PyPI](https://img.shields.io/pypi/v/m2r.svg)](https://pypi.python.org/pypi/m2r)

[![PyPI version](https://img.shields.io/pypi/pyversions/m2r.svg)](https://pypi.python.org/pypi/m2r)

[![Documentation Status](https://readthedocs.org/projects/m2r/badge/?version=latest)](http://m2r.readthedocs.io/en/latest/?badge=latest)

[![Build Status](https://travis-ci.org/miyakogi/m2r.svg?branch=master)](https://travis-ci.org/miyakogi/m2r)

[![codecov](https://codecov.io/gh/miyakogi/m2r/branch/master/graph/badge.svg)](https://codecov.io/gh/miyakogi/m2r)

--------------------------------------------------------------------------------

Markdown with reStructuredText (reST) extensions.

M2R converts a markdown including reST markups to a valid reST format.

## Features

* Basic markdown and some extensions (below)
    * inline/block embedded html
    * fenced-code block
    * tables
    * footnotes
* Inline- and Block-level reST markups
    * single- and multi-line directives (e.g. `.. directive::`)
    * inline-roles (e.g. ``:code:`print(1)` ...``)
    * ref-link (e.g. ``see `ref`_``)
    * footnotes (e.g. ``[#fn]_``)
    * math extension inspired by `recommonmark <https://recommonmark.readthedocs.io/en/latest/index.html>`_
* Sphinx support
    * ``mdinclude`` directive to include markdown from md or reST

## Installation

```
pip install m2r
```

## Usage

### Sphinx

In conf.py

```python
extensions = [
    ...,
    'm2r',
]

# source_suffix = '.rst'
source_suffix = ['.rst', '.md']
```

Write index.md and run `make html`.

#### mdinclude directive

Like `.. include:: file` directive, `.. mdinclude:: file` directive inserts markdown file at the line.

Note: do not use `.. include:: file` directive to include markdown file, use `.. mdinclude:: file` instead.

## Restrictions

* reST's directive body is parsed as reST, cannot use markdown
* Table column alignment is not supported (reST does not support this feature)

## Example

See [example in document](https://miyakogi.github.io/m2r/example.html).

## Licence

MIT
