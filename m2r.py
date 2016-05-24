#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import mistune


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
        return '\n\n.. raw:: html\n\n' + self._indent_block(html)

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
        raise NotImplementedError('sorry')
        return (
            '<table>\n<thead>%s</thead>\n'
            '<tbody>\n%s</tbody>\n</table>\n'
        ) % (header, body)

    def table_row(self, content):
        """Rendering a table row. Like ``<tr>``.

        :param content: content of current table row.
        """
        raise NotImplementedError('sorry')
        return '<tr>\n%s</tr>\n' % content

    def table_cell(self, content, **flags):
        """Rendering a table cell. Like ``<th>`` ``<td>``.

        :param content: content of current table cell.
        :param header: whether this is header or not.
        :param align: align of current table cell.
        """
        raise NotImplementedError('sorry')
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
        raise NotImplementedError('sorry')
        if self.options.get('use_xhtml'):
            return '<br />\n'
        return '<br>\n'

    def strikethrough(self, text):
        """Rendering ~~strikethrough~~ text.

        :param text: text content for strikethrough.
        """
        # not supported in rst. may be need :raw-html:`<del>%s</del>
        raise NotImplementedError('sorry')
        return '<del>%s</del>' % text

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
        return '\n\n.. image:: {src}\n   :target: {src}\n   :alt: {text}\n\n'.format(**locals())

    def inline_html(self, html):
        """Rendering span level pure html content.

        :param html: text content of the html snippet.
        """
        raise NotImplementedError('sorry')
        if self.options.get('escape'):
            return escape(html)
        return html

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


if __name__ == '__main__':
    with open('./a.md') as f:
        src = f.read()
    renderer = RestRenderer()
    markdown = mistune.Markdown(renderer)
    print(markdown(src))
