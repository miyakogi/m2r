# Example

This page is written in mixed markdown and reST.
Source code is [here](https://github.com/miyakogi/m2r/blob/master/docs/example.md).

## Basic Markups (inline)

A **strong**, *emphasis*, ~~deleted~~, `code with single-backtick`,
``code with two-backticks``, ```code can include multiple (``) backticks```,
:code:`reST's code role`, and <del>inline html</del>delete.

### Link

Auto link to http://example.com/.

Link to [example.com](http://example.com/) in markdown.

Link to [anchor](#testlabel) in markdown.

Link to [document](example.md) in markdown.

Link to [document with anchor](example.md#testlabel) in markdown (doc directive does not support anchors, so this links to the document only).

Link to `example.com <http://example.com/>`_ in reST.

Link to `example`_ in reST_ref.

Link to [example.com](http://example.com/ "example") with title in markdown.

.. _example: http://example.com


.. _testlabel:

## Basic Markups (block)

This is a simple sentence.

| sentence with
| newlines
| (reST)

Sentence with  
hard-wrap (markdown, trailing two spaces)

> block quote
> second line
> > nested quote

---

<div style="color: red;">This is a red, raw-html block.</div>

> Block quote after raw-html directive

### List

#### Unordered list

* unordered list
  new line
* next item
  * nested list
    with new line
  * nested list item 2
* original depth
  1. ordered list item
  2. second
     with new line
* original depth again

#### Ordered list

1. ordered list
   in new line
2. second item
  * nested unordered list
  * second item
    with new line
3. original depth
  1. nested ordered list
     with new line
  2. again
4. original depth again

### Code Block

Simple, indented code block

    pip install sphinx

Code block with triple backticks and language.

```python
def a(n: int) -> None:
    for i in range(n):
        print(i)
```

Triple-tildes (`~~~`) are also available.

~~~
def a(n: int) -> None:
    for i in range(n):
        print(i)
~~~

Here is reST style code block.

.. code-block:: python

    if True:
        print('\n')

## Extensions

### Table (Markdown-Style)

(cell-alignment is not supported currently)

| Table Header 1 | Table Header 2 | Table Header 3 |
|----------------|----------------|----------------|
| normal         | *italic*       | **bold**       |
| `code` | ~~deleted~~  | <b>inline-html</b> |

### Math

This is `$E = mc^2$` inline math.

The below is math-block (markdown-style).

```math
E = mc^2
```

The below is reST-style math-block.

.. math::

   E = mc^2


### Include Markdown file

To include a markdown file:

```rest
.. mdinclude:: path-to-file.md
```

To include a markdown file with a specific start and end line:

```rest
.. mdinclude:: included.md
   :start-line: 2
   :end-line: -2
```

The original ``included.md`` file is:

.. include:: included.md
   :code: md

This file is included as:

```md
#### Include this line
```

and the results in HTML are as shown below:

.. mdinclude:: included.md
   :start-line: 2
   :end-line: -2

To include a markdown file with specific line ranges:

```rest
.. mdinclude:: line_inclusion.md
   :lines: 1, 3-4, 7-
```

The original ``line_inclusion.md`` file is:

.. include:: line_inclusion.md
   :code: md

And the resulting HTML output is:

.. mdinclude:: line_inclusion.md
   :lines: 1, 3-4, 7-


To include a markdown file by specific text:

```rest
.. mdinclude:: text_inclusion.md
   :start-after: Start Here
   :end-before: End Here
```

The original ``text_inclusion.md`` file is:

.. include:: text_inclusion.md
   :code: md

And the resulting HTML output is:

.. mdinclude:: text_inclusion.md
   :start-after: Start Here
   :end-before: End Here


### Footnote

Footnote[^1] and footnote[^key] with markdown.

Footnote with reST\ [#a]_.

<!-- footnote definition -->
[^1]: footnote 1
[^key]: footnote key
.. [#a] reST footnote
