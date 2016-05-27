#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import mistune


prolog = '''\
.. m2r prolog
.. role:: raw-md-html(raw)
   :format: html

.. end of m2r prolog

'''

class RestBlockGrammar(mistune.BlockGrammar):
    directive = re.compile(
            r'^(\.\.\s+.*)\n(?=\S)',
            re.DOTALL | re.MULTILINE,
        )


class RestBlockLexer(mistune.BlockLexer):
    grammar_class = RestBlockGrammar
    default_rules = ['directive'] + mistune.BlockLexer.default_rules

    def parse_directive(self, m):
        self.tokens.append({
            'type': 'directive',
            'text': m.group(1),
        })


class RestInlineGrammar(mistune.InlineGrammar):
    rest_link = re.compile(r'`(.*?)`_')


class RestInlineLexer(mistune.InlineLexer):
    grammar_class = RestInlineGrammar
    default_rules = ['rest_link'] + mistune.InlineLexer.default_rules

    def output_rest_link(self, m):
        text = m.group(1)
        return self.renderer.rest_link(text)

    def output_directive(self, m):
        return self.renderer.directive(m.group(1))


class RestRenderer(mistune.Renderer):
    list_indent_re = re.compile(r'^(\s*(#\.|\*)\s)')
    indent = ' ' * 3
    list_marker = '{#__rest_list_mark__#}'
    hmarks = {
        1: '=',
        2: '-',
        3: '^',
        4: '~',
        5: '"',
        6: '#',
    }

    def _indent_block(self, block):
        return '\n'.join(self.indent + line  if line else '' for line in block.splitlines())

    def _raw_html(self, html):
        return ':raw-md-html:`{}`'.format(html)

    def block_code(self, code, lang=None):
        if lang:
            first_line = '\n.. code-block:: {}\n\n'.format(lang)
        else:
            first_line = '\n.. code-block::\n\n'
        return first_line + self._indent_block(code) + '\n'

    def block_quote(self, text):
        # text includes some empty line
        return '\n\n{}\n\n'.format(self._indent_block(text.strip('\n')))

    def block_html(self, html):
        """Rendering block level pure html content.

        :param html: text content of the html snippet.
        """
        return '\n\n.. raw:: html\n\n' + self._indent_block(html) + '\n\n'

    def header(self, text, level, raw=None):
        """Rendering header/heading tags like ``<h1>`` ``<h2>``.

        :param text: rendered text content for the header.
        :param level: a number for the header level, for example: 1.
        :param raw: raw text content of the header.
        """
        return '\n{0}\n{1}\n'.format(text, self.hmarks[level] * len(text))

    def hrule(self):
        """Rendering method for ``<hr>`` tag."""
        return '\n----\n'

    def list(self, body, ordered=True):
        """Rendering list tags like ``<ul>`` and ``<ol>``.

        :param body: body contents of the list.
        :param ordered: whether this list is ordered or not.
        """
        from pprint import pprint as pp
        mark = '#. ' if ordered else '* '
        lines = body.splitlines()
        for i, line in enumerate(lines):
            _l = line.lstrip()
            if line and not line.startswith(self.list_marker):
                lines[i] = ' ' * len(mark) + line
        return '\n{}\n'.format('\n'.join(lines)).replace(self.list_marker, mark)

    def list_item(self, text):
        """Rendering list item snippet. Like ``<li>``."""
        return '\n' + self.list_marker + text

    def paragraph(self, text):
        """Rendering paragraph tags. Like ``<p>``."""
        return '\n' + text + '\n'

    def table(self, header, body):
        """Rendering table element. Wrap header and body in it.

        :param header: header part of the table.
        :param body: body part of the table.
        """
        table = ('<table>\n<thead>\n{0}</thead>\n'
                 '<tbody>\n{1}</tbody>\n</table>').format(header, body)
        return '\n\n.. raw:: html\n\n' + self._indent_block(table) + '\n\n'

    def table_row(self, content):
        """Rendering a table row. Like ``<tr>``.

        :param content: content of current table row.
        """
        return '<tr>\n%s</tr>\n' % content

    def table_cell(self, content, **flags):
        """Rendering a table cell. Like ``<th>`` ``<td>``.

        :param content: content of current table cell.
        :param header: whether this is header or not.
        :param align: align of current table cell.
        """
        if flags['header']:
            tag = 'th'
        else:
            tag = 'td'
        align = flags['align']
        if not align:
            return '<%s>%s</%s>\n' % (tag, content, tag)
        return '<%s style="text-align:%s">%s</%s>\n' % (
            tag, align, content, tag
        )

    def double_emphasis(self, text):
        """Rendering **strong** text.

        :param text: text content for emphasis.
        """
        return '**{}**'.format(text)

    def emphasis(self, text):
        """Rendering *emphasis* text.

        :param text: text content for emphasis.
        """
        return '*{}*'.format(text)

    def codespan(self, text):
        """Rendering inline `code` text.

        :param text: text content for inline code.
        """
        return '``{}``'.format(text)

    def linebreak(self):
        """Rendering line break like ``<br>``."""
        if self.options.get('use_xhtml'):
            return self._raw_html('<br />') + '\n'
        return self._raw_html('<br>') + '\n'

    def strikethrough(self, text):
        """Rendering ~~strikethrough~~ text.

        :param text: text content for strikethrough.
        """
        return self._raw_html('<del>{}</del>'.format(text))

    def text(self, text):
        """Rendering unformatted text.

        :param text: text content.
        """
        return text

    def autolink(self, link, is_email=False):
        """Rendering a given link or email address.

        :param link: link content or email address.
        :param is_email: whether this is an email or not.
        """
        return link

    def link(self, link, title, text):
        """Rendering a given link with content and title.

        :param link: href link for ``<a>`` tag.
        :param title: title content for `title` attribute.
        :param text: text content for description.
        """
        if title:
            raise NotImplementedError('sorry')
        return '`{text} <{target}>`_'.format(target=link, text=text)

    def image(self, src, title, text):
        """Rendering a image with title and text.

        :param src: source link of the image.
        :param title: title text of the image.
        :param text: alt text of the image.
        """
        # rst not support title option, and I couldn't find title attribute in HTML standard
        return '\n\n.. image:: {src}\n   :target: {src}\n   :alt: {text}\n\n'.format(**locals())

    def inline_html(self, html):
        """Rendering span level pure html content.

        :param html: text content of the html snippet.
        """
        if self.options.get('escape'):
            html = escape(html)
        return self._raw_html(html)

    def newline(self):
        """Rendering newline element."""
        return ''

    def footnote_ref(self, key, index):
        """Rendering the ref anchor of a footnote.

        :param key: identity key for the footnote.
        :param index: the index count of current footnote.
        """
        raise NotImplementedError('sorry')
        html = (
            '<sup class="footnote-ref" id="fnref-%s">'
            '<a href="#fn-%s" rel="footnote">%d</a></sup>'
        ) % (escape(key), escape(key), index)
        return html

    def footnote_item(self, key, text):
        """Rendering a footnote item.

        :param key: identity key for the footnote.
        :param text: text content of the footnote.
        """
        raise NotImplementedError('sorry')
        back = (
            '<a href="#fnref-%s" rev="footnote">&#8617;</a>'
        ) % escape(key)
        text = text.rstrip()
        if text.endswith('</p>'):
            text = re.sub(r'<\/p>$', r'%s</p>' % back, text)
        else:
            text = '%s<p>%s</p>' % (text, back)
        html = '<li id="fn-%s">%s</li>\n' % (escape(key), text)
        return html

    def footnotes(self, text):
        """Wrapper for all footnotes.

        :param text: contents of all footnotes.
        """
        raise NotImplementedError('sorry')
        html = '<div class="footnotes">\n%s<ol>%s</ol>\n</div>\n'
        return html % (self.hrule(), text)

    """Below outputs are for rst."""
    def rest_link(self, text):
        return '`{}`_'.format(text)

    def directive(self, text):
        return '\n' + text + '\n'


class M2R(mistune.Markdown):
    def __init__(self, renderer=None, inline=RestInlineLexer, block=RestBlockLexer, **kwargs):
        if renderer is None:
            renderer = RestRenderer(**kwargs)
        super().__init__(renderer, inline=inline, block=block, **kwargs)

    def output_directive(self):
        return self.renderer.directive(self.token['text'])


if __name__ == '__main__':
    with open('./a.md') as f:
        src = f.read()
    renderer = RestRenderer()
    markdown = mistune.Markdown(renderer)
    print(markdown(src))
