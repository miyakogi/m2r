#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase, skip

from docutils.core import Publisher
from docutils import io
from mistune import Markdown

from m2r import RestRenderer, RestInlineLexer, RestBlockLexer, M2R


class RendererTestBase(TestCase):
    def setUp(self):
        self.md = M2R()

    def conv(self, src:str):
        out = self.md(src)
        self.check_rst(out)
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


class TestInlineMarkdown(RendererTestBase):
    def test_inline_code(self):
        src = '`a`'
        out = self.conv(src)
        self.assertEqual(out.replace('\n', ''), '``a``')

    def test_emphasis(self):
        src = '*a*'
        out = self.conv(src)
        self.assertEqual(out.replace('\n', ''), '*a*')

    def test_double_emphasis(self):
        src = '**a**'
        out = self.conv(src)
        self.assertEqual(out.replace('\n', ''), '**a**')

    def test_autolink(self):
        src = 'link to http://example.com/ in sentence.'
        out = self.conv(src)
        self.assertEqual(out, '\n' + src + '\n')

    def test_link(self):
        src = 'this is a [link](http://example.com/).'
        out = self.conv(src)
        self.assertEqual(out, '\nthis is a `link <http://example.com/>`_.\n')

    def test_rest_link(self):
        src = '`RefLink <http://example.com>`_'
        out = self.conv(src)


class TestBlockQuote(RendererTestBase):
    def test_block_quote(self):
        src = '> q1\n> q2'
        out = self.conv(src)
        self.assertEqual(out, '\n\n   q1\n   q2\n\n')

    def test_block_quote_nested(self):
        src = '> q1\n> > q2'
        out = self.conv(src)
        # one extra empty line is inserted, but still valid rst anyway
        self.assertEqual(out, '\n\n   q1\n\n\n      q2\n\n')

    @skip('markdown does not support dedent in block quote')
    def test_block_quote_nested_2(self):
        src = '> q1\n> > q2\n> q3'
        out = self.conv(src)
        self.assertEqual(out, '\n\n   q1\n\n      q2\n\n   q3\n\n')



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

    def test_plain_code_block_indent(self):
        src = '\n'.join([
            '```',
            'pip install sphinx',
            '    new line',
            '```',
        ])
        out = self.conv(src)
        self.assertEqual(out, '\n.. code-block::\n\n   pip install sphinx\n       new line\n')

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
        self.assertEqual(out, '\n.. code-block:: python\n\n   def a(i):\n       print(i)\n')


class TestImage(RendererTestBase):
    def test_image(self):
        src = '![alt text](a.png)'
        out = self.conv(src)
        # first and last newline is inserted by paragraph
        self.assertEqual(out, '\n\n\n.. image:: a.png\n   :target: a.png\n   :alt: alt text\n\n\n')

    def test_image_tiele(self):
        src = '![alt text](a.png "title")'
        out = self.conv(src)
        # title is not supported now


class TestHeading(RendererTestBase):
    def test_heading(self):
        src = '# head 1'
        out = self.conv(src)
        self.assertEqual(out, '\nhead 1\n' + '=' * 6 + '\n')


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
        self.assertEqual(out, '\n\n* list 1\n* list 2\n\n  * list 2.1\n  * list 2.2\n\n* list 3\n')

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
        self.assertEqual(out, '\n\n#. list 1\n#. list 2\n\n   #. list 2.1\n   #. list 2.2\n\n#. list 3\n')

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
        out = self.conv(src)


class TestTable(RendererTestBase):
    def test_table(self):
        src = '''h1 | h2 | h3\n--- | --- | ---\n1 | 2 | 3\n4 | 5 | 6'''
        out = self.conv(src)
        self.assertEqual(out, '\n'.join([
            '',
            '',
            '.. raw:: html',
            '',
            '   <table>',
            '   <thead>',
            '   <tr>',
            '   <th>h1</th>',
            '   <th>h2</th>',
            '   <th>h3</th>',
            '   </tr>',
            '   </thead>',
            '   <tbody>',
            '   <tr>',
            '   <td>1</td>',
            '   <td>2</td>',
            '   <td>3</td>',
            '   </tr>',
            '   <tr>',
            '   <td>4</td>',
            '   <td>5</td>',
            '   <td>6</td>',
            '   </tr>',
            '   </tbody>',
            '   </table>',
            '',
            '',
        ]))


class TestDirective(RendererTestBase):
    def test_comment_oneline(self):
        src = '.. a'
        out = self.conv(src)
        self.assertEqual(out, '\n.. a\n')

    def test_comment_multiline(self):
        comment = ('.. this is comment.\n   this is also comment.\n\n\n'
               '    comment may include empty line.\n'
               '\n\n')
        src = comment + '`eoc`'
        out = self.conv(src)
        self.assertEqual(out, '\n' + comment + '``eoc``\n')
