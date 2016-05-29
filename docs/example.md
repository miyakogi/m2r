# Example

This page is written in mixed markdown and reST.
Source code is [here](https://github.com/miyakogi/m2r/blob/master/docs/example.md).

## Basic Markups (inline)

A **strong**, *emphasis*, ~~deleted~~, `code with single-backtick`,
``code with two-backtick``, :code:`rest's code role`, and <del>inline html</del>delete.

### Link

Auto link to http://example.com/.

Link to [example.com](http://example.com/) in markdown.

Link to `example.com <http://example.com/>`_ in rest.

Link to `example`_ in rest_ref.

.. _example: http://example.com


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

Code block with triple backticks.

```python
def a(n: int) -> None:
    for i in range(n):
        print(i)
```

Rest style code block.

.. code-block:: python

   print('\n')

## Extensions

### Table (markdown)

| Table Header 1 | Table Header 2 | Table Header 3 |
|:---------------|:--------------:|---------------:|
| left           | center         | right          |

### Math

This is `$E = mc^2$` inline math.

The below is math-block (markdown).

```math
E = mc^2
```

The below is math-block (rest).

.. math::

   E = mc^2

### Footnote

Footnote[^1] and footnote[^key] with markdown.

Footnote with rest\ [#a]_.

[^1]: footnote 1
[^key]: footnote key

.. [#a] rest footnote
