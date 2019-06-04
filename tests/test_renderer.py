#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from unittest import TestCase, skip

from docutils.core import Publisher
from docutils import io

from m2r import prolog, convert


class RendererTestBase(TestCase):
    def conv(self, src, **kwargs):
        out = convert(src, **kwargs)
        self.check_rst(out)
        return out

    def conv_no_check(self, src, **kwargs):
        out = convert(src, **kwargs)
        return out

    def check_rst(self, rst):
        pub = Publisher(reader=None, parser=None, writer=None, settings=None,
                        source_class=io.StringInput,
                        destination_class=io.StringOutput)
        pub.set_components(reader_name='standalone',
                           parser_name='restructuredtext',
                           writer_name='pseudoxml')
        pub.process_programmatic_settings(
            settings_spec=None,
            settings_overrides={'output_encoding': 'unicode'},
            config_section=None,
        )
        pub.set_source(rst, source_path=None)
        pub.set_destination(destination=None, destination_path=None)
        output = pub.publish(enable_exit_status=False)
        self.assertLess(pub.document.reporter.max_level, 0)
        return output, pub


class TestBasic(RendererTestBase):
    def test_fail_rst(self):
        with self.assertRaises(AssertionError):
            # This check should be failed and report warning
            self.check_rst('```')

    def test_simple_paragraph(self):
        src = 'this is a sentence.\n'
        out = self.conv(src)
        self.assertEqual(out, '\n' + src)

    def test_multiline_paragraph(self):
        src = '\n'.join([
            'first sentence.',
            'second sentence.',
        ])
        out = self.conv(src)
        self.assertEqual(out, '\n' + src + '\n')

    def test_multi_paragraph(self):
        src = '\n'.join([
            'first paragraph.',
            '',
            'second paragraph.',
        ])
        out = self.conv(src)
        self.assertEqual(out, '\n' + src + '\n')

    def test_hr(self):
        src = 'a\n\n---\n\nb'
        out = self.conv(src)
        self.assertEqual(out, '\na\n\n----\n\nb\n')

    def test_linebreak(self):
        src = 'abc def  \nghi'
        out = self.conv(src)
        self.assertEqual(
            out,
            prolog + '\nabc def\\ :raw-html-m2r:`<br>`\nghi' + '\n',
        )


class TestInlineMarkdown(RendererTestBase):
    def test_inline_code(self):
        src = '`a`'
        out = self.conv(src)
        self.assertEqual(out.replace('\n', ''), '``a``')

    def test_inline_code_with_backticks(self):
        src = '```a``a```'
        out = self.conv(src)
        self.assertEqual(out.strip(),
                         '.. role:: raw-html-m2r(raw)\n'
                         '   :format: html\n\n\n'
                         ':raw-html-m2r:`<code class="docutils literal">'
                         '<span class="pre">a&#96;&#96;a</span></code>`'
                         )

    def test_strikethrough(self):
        src = ('~~a~~')
        self.conv(src)

    def test_emphasis(self):
        src = '*a*'
        out = self.conv(src)
        self.assertEqual(out.replace('\n', ''), '*a*')

    def test_emphasis_(self):
        src = '_a_'
        out = self.conv(src)
        self.assertEqual(out.replace('\n', ''), '*a*')

    def test_emphasis_no_(self):
        src = '_a_'
        out = self.conv(src, no_underscore_emphasis=True)
        self.assertEqual(out.replace('\n', ''), '_a_')

    def test_double_emphasis(self):
        src = '**a**'
        out = self.conv(src)
        self.assertEqual(out.replace('\n', ''), '**a**')

    def test_double_emphasis__(self):
        src = '__a__'
        out = self.conv(src)
        self.assertEqual(out.replace('\n', ''), '**a**')

    def test_emphasis_no__(self):
        src = '__a__'
        out = self.conv(src, no_underscore_emphasis=True)
        self.assertEqual(out.replace('\n', ''), '__a__')

    def test_autolink(self):
        src = 'link to http://example.com/ in sentence.'
        out = self.conv(src)
        self.assertEqual(out, '\n' + src + '\n')

    def test_link(self):
        src = 'this is a [link](http://example.com/).'
        out = self.conv(src)
        self.assertEqual(
            out, '\nthis is a `link <http://example.com/>`_.\n')

    def test_anonymous_link(self):
        src = 'this is a [link](http://example.com/).'
        out = self.conv(src, anonymous_references=True)
        self.assertEqual(
            out, '\nthis is a `link <http://example.com/>`__.\n')

    def test_link_with_rel_link_enabled(self):
        src = 'this is a [link](http://example.com/).'
        out = self.conv_no_check(
            src,
            parse_relative_links=True
        )
        self.assertEqual(
            out, '\nthis is a `link <http://example.com/>`_.\n')

    def test_anonymous_link_with_rel_link_enabled(self):
        src = 'this is a [link](http://example.com/).'
        out = self.conv_no_check(
            src,
            parse_relative_links=True,
            anonymous_references=True
        )
        self.assertEqual(
            out, '\nthis is a `link <http://example.com/>`__.\n')

    def test_anchor(self):
        src = 'this is an [anchor](#anchor).'
        out = self.conv_no_check(
            src,
            parse_relative_links=True
        )
        self.assertEqual(
            out, '\nthis is an :ref:`anchor <anchor>`.\n')

    def test_relative_link(self):
        src = 'this is a [relative link](a_file.md).'
        out = self.conv_no_check(
            src,
            parse_relative_links=True
        )
        self.assertEqual(
            out, '\nthis is a :doc:`relative link <a_file>`.\n')

    def test_relative_link_with_anchor(self):
        src = 'this is a [relative link](a_file.md#anchor).'
        out = self.conv_no_check(
            src,
            parse_relative_links=True
        )
        self.assertEqual(
            out, '\nthis is a :doc:`relative link <a_file>`.\n')

    def test_link_title(self):
        src = 'this is a [link](http://example.com/ "example").'
        out = self.conv(src)
        self.assertEqual(
            out,
            '.. role:: raw-html-m2r(raw)\n'
            '   :format: html\n\n\n'
            'this is a :raw-html-m2r:'
            '`<a href="http://example.com/" title="example">link</a>`.\n'
        )

    def test_image_link(self):
        src = '[![Alt Text](image_taget_url)](link_target_url)'
        out = self.conv(src)
        self.assertEqual(
            out,
            '\n\n.. image:: image_taget_url\n'
            '   :target: link_target_url\n   :alt: Alt Text\n\n',
        )

    def test_rest_role(self):
        src = 'a :code:`some code` inline.'
        out = self.conv(src)
        self.assertEqual(out, '\n' + src + '\n')

    def test_rest_role2(self):
        src = 'a `some code`:code: inline.'
        out = self.conv(src)
        self.assertEqual(out, '\n' + src + '\n')

    def test_rest_link(self):
        src = 'a `RefLink <http://example.com>`_ here.'
        out = self.conv(src)
        self.assertEqual(out, '\n' + src + '\n')

    def test_rest_link_and_role(self):
        src = 'a :code:`a` and `RefLink <http://example.com>`_ here.'
        out = self.conv(src)
        self.assertEqual(out, '\n' + src + '\n')

    def test_rest_link_and_role2(self):
        src = 'a `a`:code: and `RefLink <http://example.com>`_ here.'
        out = self.conv(src)
        self.assertEqual(out, '\n' + src + '\n')

    def test_rest_role_incomplete(self):
        src = 'a co:`de` and `RefLink <http://example.com>`_ here.'
        out = self.conv(src)
        self.assertEqual(
            out,
            '\na co:\\ ``de`` and `RefLink <http://example.com>`_ here.\n',
        )

    def test_rest_role_incomplete2(self):
        src = 'a `RefLink <http://example.com>`_ and co:`de` here.'
        out = self.conv(src)
        self.assertEqual(
            out,
            '\na `RefLink <http://example.com>`_ and co:\\ ``de`` here.\n',
        )

    def test_rest_role_with_code(self):
        src = 'a `code` and :code:`rest` here.'
        out = self.conv(src)
        self.assertEqual(out, '\na ``code`` and :code:`rest` here.\n')

    def test_rest2_role_with_code(self):
        src = 'a `code` and `rest`:code: here.'
        out = self.conv(src)
        self.assertEqual(out, '\na ``code`` and `rest`:code: here.\n')

    def test_code_with_rest_role(self):
        src = 'a :code:`rest` and `code` here.'
        out = self.conv(src)
        self.assertEqual(out, '\na :code:`rest` and ``code`` here.\n')

    def test_code_with_rest_role2(self):
        src = 'a `rest`:code: and `code` here.'
        out = self.conv(src)
        self.assertEqual(out, '\na `rest`:code: and ``code`` here.\n')

    def test_rest_link_with_code(self):
        src = 'a `RefLink <a>`_ and `code` here.'
        out = self.conv(src)
        self.assertEqual(out, '\na `RefLink <a>`_ and ``code`` here.\n')

    def test_code_with_rest_link(self):
        src = 'a `code` and `RefLink <a>`_ here.'
        out = self.conv(src)
        self.assertEqual(out, '\na ``code`` and `RefLink <a>`_ here.\n')

    def test_inline_math(self):
        src = 'this is `$E = mc^2$` inline math.'
        out = self.conv(src)
        self.assertEqual(out, '\nthis is :math:`E = mc^2` inline math.\n')

    def test_disable_inline_math(self):
        src = 'this is `$E = mc^2$` inline math.'
        out = self.conv(src, disable_inline_math=True)
        self.assertEqual(out, '\nthis is ``$E = mc^2$`` inline math.\n')

    def test_inline_html(self):
        src = 'this is <s>html</s>.'
        out = self.conv(src)
        self.assertEqual(
            out, prolog + '\nthis is :raw-html-m2r:`<s>html</s>`.\n')

    def test_block_html(self):
        src = '<h1>title</h1>'
        out = self.conv(src)
        self.assertEqual(out, '\n\n.. raw:: html\n\n   <h1>title</h1>\n\n')


class TestBlockQuote(RendererTestBase):
    def test_block_quote(self):
        src = '> q1\n> q2'
        out = self.conv(src)
        self.assertEqual(out, '\n..\n\n   q1\n   q2\n\n')

    def test_block_quote_nested(self):
        src = '> q1\n> > q2'
        out = self.conv(src)
        # one extra empty line is inserted, but still valid rst anyway
        self.assertEqual(out, '\n..\n\n   q1\n\n   ..\n\n      q2\n\n')

    @skip('markdown does not support dedent in block quote')
    def test_block_quote_nested_2(self):
        src = '> q1\n> > q2\n> q3'
        out = self.conv(src)
        self.assertEqual(out, '\n..\n\n   q1\n\n   ..\n      q2\n\n   q3\n\n')


class TestCodeBlock(RendererTestBase):
    def test_plain_code_block(self):
        src = '\n'.join([
            '```',
            'pip install sphinx',
            '```',
        ])
        out = self.conv(src)
        self.assertEqual(out, '\n.. code-block::\n\n   pip install sphinx\n')

    def test_plain_code_block_tilda(self):
        src = '\n'.join([
            '~~~',
            'pip install sphinx',
            '~~~',
        ])
        out = self.conv(src)
        self.assertEqual(out, '\n.. code-block::\n\n   pip install sphinx\n')

    def test_code_block_math(self):
        src = '\n'.join([
            '```math',
            'E = mc^2',
            '```',
        ])
        out = self.conv(src)
        self.assertEqual(out, '\n.. math::\n\n   E = mc^2\n')

    def test_plain_code_block_indent(self):
        src = '\n'.join([
            '```',
            'pip install sphinx',
            '    new line',
            '```',
        ])
        out = self.conv(src)
        self.assertEqual(
            out,
            '\n.. code-block::\n\n   pip install sphinx\n       new line\n',
        )

    def test_python_code_block(self):
        src = '\n'.join([
            '```python',
            'print(1)',
            '```',
        ])
        out = self.conv(src)
        self.assertEqual(out, '\n.. code-block:: python\n\n   print(1)\n')

    def test_python_code_block_indent(self):
        src = '\n'.join([
            '```python',
            'def a(i):',
            '    print(i)',
            '```',
        ])
        out = self.conv(src)
        self.assertEqual(
            out,
            '\n.. code-block:: python\n\n   def a(i):\n       print(i)\n',
        )


class TestImage(RendererTestBase):
    def test_image(self):
        src = '![alt text](a.png)'
        out = self.conv(src)
        # first and last newline is inserted by paragraph
        self.assertEqual(
            out,
            '\n\n.. image:: a.png\n   :target: a.png\n   :alt: alt text\n\n',
        )

    def test_image_title(self):
        src = '![alt text](a.png "title")'
        self.conv(src)
        # title is not supported now


class TestHeading(RendererTestBase):
    def test_heading(self):
        src = '# head 1'
        out = self.conv(src)
        self.assertEqual(out, '\nhead 1\n' + '=' * 6 + '\n')

    def test_heading_multibyte(self):
        src = '# マルチバイト文字\n'
        out = self.conv(src)
        self.assertEqual(out, '\nマルチバイト文字\n' + '=' * 16 + '\n')


class TestList(RendererTestBase):
    def test_ul(self):
        src = '* list'
        out = self.conv(src)
        self.assertEqual(out, '\n\n* list\n')

    def test_ol(self):
        src = '1. list'
        out = self.conv(src)
        self.assertEqual(out, '\n\n#. list\n')

    def test_nested_ul(self):
        src = '\n'.join([
            '* list 1',
            '* list 2',
            '  * list 2.1',
            '  * list 2.2',
            '* list 3',
        ])
        out = self.conv(src)
        self.assertEqual(
            out,
            '\n\n* list 1\n'
            '* list 2\n\n'
            '  * list 2.1\n'
            '  * list 2.2\n\n'
            '* list 3\n',
        )

    def test_nested_ul_2(self):
        src = '\n'.join([
            '* list 1',
            '* list 2',
            '  * list 2.1',
            '  * list 2.2',
            '    * list 2.2.1',
            '    * list 2.2.2',
            '* list 3',
        ])
        out = self.conv(src)
        self.assertEqual(
            out,
            '\n\n* list 1\n'
            '* list 2\n\n'
            '  * list 2.1\n'
            '  * list 2.2\n\n'
            '    * list 2.2.1\n'
            '    * list 2.2.2\n\n'
            '* list 3\n'
        )

    def test_nested_ol(self):
        src = '\n'.join([
            '1. list 1',
            '2. list 2',
            '  2. list 2.1',
            '  3. list 2.2',
            '3. list 3',
        ])
        out = self.conv(src)
        self.assertEqual(
            out,
            '\n\n#. list 1\n'
            '#. list 2\n'
            '\n'
            '   #. list 2.1\n'
            '   #. list 2.2\n'
            '\n'
            '#. list 3\n',
        )

    def test_nested_ol_2(self):
        src = '\n'.join([
            '1. list 1',
            '2. list 2',
            '  3. list 2.1',
            '  4. list 2.2',
            '    5. list 2.2.1',
            '    6. list 2.2.2',
            '7. list 3',
        ])
        out = self.conv(src)
        self.assertEqual(
            out,
            '\n'.join([
                '\n\n#. list 1',
                '#. list 2',
                '',
                '   #. list 2.1',
                '   #. list 2.2',
                '',
                '      #. list 2.2.1',
                '      #. list 2.2.2',
                '',
                '#. list 3\n',
            ])
        )

    def test_nested_mixed_1(self):
        src = '\n'.join([
            '1. list 1',
            '2. list 2',
            '  * list 2.1',
            '  * list 2.2',
            '    1. list 2.2.1',
            '    2. list 2.2.2',
            '7. list 3',
        ])
        out = self.conv(src)
        self.assertEqual(
            out,
            '\n'.join([
                '\n\n#. list 1',
                '#. list 2',
                '',
                '   * list 2.1',
                '   * list 2.2',
                '',
                '     #. list 2.2.1',
                '     #. list 2.2.2',
                '',
                '#. list 3\n',
            ])
        )

    def test_nested_multiline_1(self):
        src = '\n'.join([
            '* list 1',
            '  list 1 cont',
            '* list 2',
            '  list 2 cont',
            '  * list 2.1',
            '    list 2.1 cont',
            '  * list 2.2',
            '    list 2.2 cont',
            '    * list 2.2.1',
            '    * list 2.2.2',
            '* list 3',
        ])
        out = self.conv(src)
        self.assertEqual(
            out,
            '\n'.join([
                '\n\n* list 1',
                '  list 1 cont',
                '* list 2',
                '  list 2 cont',
                '',
                '  * list 2.1',
                '    list 2.1 cont',
                '  * list 2.2',
                '    list 2.2 cont',
                '',
                '    * list 2.2.1',
                '    * list 2.2.2',
                '',
                '* list 3\n',
            ])
        )

    def test_nested_multiline_2(self):
        src = '\n'.join([
            '1. list 1',
            '  list 1 cont',
            '1. list 2',
            '  list 2 cont',
            '  1. list 2.1',
            '    list 2.1 cont',
            '  1. list 2.2',
            '    list 2.2 cont',
            '    1. list 2.2.1',
            '    1. list 2.2.2',
            '1. list 3',
        ])
        out = self.conv(src)
        self.assertEqual(
            out,
            '\n'.join([
                '\n\n#. list 1',
                '   list 1 cont',
                '#. list 2',
                '   list 2 cont',
                '',
                '   #. list 2.1',
                '      list 2.1 cont',
                '   #. list 2.2',
                '      list 2.2 cont',
                '',
                '      #. list 2.2.1',
                '      #. list 2.2.2',
                '',
                '#. list 3\n',
            ])
        )

    def test_nested_multiline_3(self):
        src = '\n'.join([
            '1. list 1',
            '  list 1 cont',
            '1. list 2',
            '  list 2 cont',
            '  * list 2.1',
            '    list 2.1 cont',
            '  * list 2.2',
            '    list 2.2 cont',
            '    1. list 2.2.1',
            '    1. list 2.2.2',
            '1. list 3',
        ])
        out = self.conv(src)
        self.assertEqual(
            out,
            '\n'.join([
                '\n\n#. list 1',
                '   list 1 cont',
                '#. list 2',
                '   list 2 cont',
                '',
                '   * list 2.1',
                '     list 2.1 cont',
                '   * list 2.2',
                '     list 2.2 cont',
                '',
                '     #. list 2.2.1',
                '     #. list 2.2.2',
                '',
                '#. list 3\n',
            ])
        )


class TestConplexText(RendererTestBase):
    def test_code(self):
        src = '''
some sentence
```python
print(1)
```
some sentence

# title
```python
print(1)
```
---
end
'''
        self.conv(src)


class TestTable(RendererTestBase):
    def test_table(self):
        src = '''h1 | h2 | h3\n--- | --- | ---\n1 | 2 | 3\n4 | 5 | 6'''
        out = self.conv(src)
        self.assertEqual(out, '\n'.join([
            '',
            '.. list-table::',
            '   :header-rows: 1',
            '',
            '   * - h1',
            '     - h2',
            '     - h3',
            '   * - 1',
            '     - 2',
            '     - 3',
            '   * - 4',
            '     - 5',
            '     - 6',
            '',
            '',
        ]))


class TestFootNote(RendererTestBase):
    def test_footnote(self):
        src = '\n'.join([
            'This is a[^1] footnote[^2] ref[^ref] with rst [#a]_.',
            '',
            '[^1]: note 1',
            '[^2]: note 2',
            '[^ref]: note ref',
            '.. [#a] note rst',
        ])
        out = self.conv(src)
        self.assertEqual(out, '\n'.join([
            '',
            'This is a\\ [#fn-1]_ '
            'footnote\\ [#fn-2]_ ref\\ [#fn-ref]_ with rst [#a]_.',
            '',
            '.. [#a] note rst',  # one empty line inserted...
            '',
            '.. [#fn-1] note 1',
            '.. [#fn-2] note 2',
            '.. [#fn-ref] note ref',
            '',
        ]))

    def test_sphinx_ref(self):
        src = 'This is a sphinx [ref]_ global ref.\n\n.. [ref] ref text'
        out = self.conv(src)
        self.assertEqual(out, '\n' + src)


class TestDirective(RendererTestBase):
    def test_comment_oneline(self):
        src = '.. a'
        out = self.conv(src)
        self.assertEqual(out, '\n.. a')

    def test_comment_indented(self):
        src = '    .. a'
        out = self.conv(src)
        self.assertEqual(out, '\n    .. a')

    def test_comment_newline(self):
        src = '..\n\n   comment\n\nnewline'
        out = self.conv(src)
        self.assertEqual(out, '\n..\n\n   comment\n\nnewline\n')

    def test_comment_multiline(self):
        comment = (
            '.. this is comment.\n'
            '   this is also comment.\n'
            '\n'
            '\n'
            '    comment may include empty line.\n'
            '\n\n')
        src = comment + '`eoc`'
        out = self.conv(src)
        self.assertEqual(out, '\n' + comment + '``eoc``\n')


class TestRestCode(RendererTestBase):
    def test_rest_code_block_empty(self):
        src = '\n\n::\n\n'
        out = self.conv(src)
        self.assertEqual(out, '\n\n')

    def test_eol_marker(self):
        src = 'a::\n\n    code\n'
        out = self.conv(src)
        self.assertEqual(out, '\na:\n\n.. code-block::\n\n   code\n')

    def test_eol_marker_remove(self):
        src = 'a ::\n\n    code\n'
        out = self.conv(src)
        self.assertEqual(out, '\na\n\n.. code-block::\n\n   code\n')
