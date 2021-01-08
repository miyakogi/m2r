#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import sys
import os
from os import path
from copy import copy
from unittest import TestCase
import subprocess

from m2r import parse_from_file, main, options

if sys.version_info < (3, ):
    from mock import patch
    _builtin = '__builtin__'
    from codecs import open as _open
    from functools import partial
    open = partial(_open, encoding='utf-8')
else:
    from unittest.mock import patch
    _builtin = 'builtins'

curdir = path.dirname(path.abspath(__file__))
test_md = path.join(curdir, 'test.md')
test_rst = path.join(curdir, 'test.rst')


class TestConvert(TestCase):
    def setUp(self):
        # reset cli options
        options.overwrite = False
        options.dry_run = False
        options.no_underscore_emphasis = False
        options.anonymous_references = False
        options.disable_inline_math = False
        self._orig_argv = copy(sys.argv)
        if path.exists(test_rst):
            with open(test_rst) as f:
                self._orig_rst = f.read()

    def tearDown(self):
        sys.argv = self._orig_argv
        with open(test_rst, 'w') as f:
            f.write(self._orig_rst)

    def test_no_file(self):
        p = subprocess.Popen(
            [sys.executable, '-m', 'm2r'],
            stdout=subprocess.PIPE,
        )
        p.wait()
        self.assertEqual(p.returncode, 0)
        with p.stdout as buffer:
            message = buffer.read().decode()
        self.assertIn('usage', message)
        self.assertIn('underscore-emphasis', message)
        self.assertIn('anonymous-references', message)
        self.assertIn('inline-math', message)
        self.assertRegex(message, r'option(s|al arguments):')

    def test_parse_file(self):
        output = parse_from_file(test_md)
        with open(test_rst) as f:
            expected = f.read()
        self.assertEqual(output.strip(), expected.strip())

    def test_dryrun(self):
        sys.argv = [sys.argv[0], '--dry-run', test_md]
        target_file = path.join(curdir, 'test.rst')
        with open(target_file) as f:
            rst = f.read()
        os.remove(target_file)
        self.assertFalse(path.exists(target_file))
        with patch(_builtin + '.print') as m:
            main()
        self.assertFalse(path.exists(target_file))
        m.assert_called_once_with(rst)

    def test_write_file(self):
        sys.argv = [sys.argv[0], test_md]
        target_file = path.join(curdir, 'test.rst')
        os.remove(target_file)
        self.assertFalse(path.exists(target_file))
        main()
        self.assertTrue(path.exists(target_file))

    def test_overwrite_file(self):
        sys.argv = [sys.argv[0], test_md]
        target_file = path.join(curdir, 'test.rst')
        with open(target_file, 'w') as f:
            f.write('test')
        with open(target_file) as f:
            first_line = f.readline()
        self.assertIn('test', first_line)
        with patch(_builtin + '.input', return_value='y'):
            main()
        self.assertTrue(path.exists(target_file))
        with open(target_file) as f:
            first_line = f.readline()
        self.assertNotIn('test', first_line)

    def test_overwrite_option(self):
        sys.argv = [sys.argv[0], '--overwrite', test_md]
        target_file = path.join(curdir, 'test.rst')
        with open(target_file, 'w') as f:
            f.write('test')
        with open(target_file) as f:
            first_line = f.readline()
        self.assertIn('test', first_line)
        with patch(_builtin + '.input', return_value='y') as m_input:
            with patch(_builtin + '.print') as m_print:
                main()
        self.assertTrue(path.exists(target_file))
        self.assertFalse(m_input.called)
        self.assertFalse(m_print.called)
        with open(target_file) as f:
            first_line = f.readline()
        self.assertNotIn('test', first_line)

    def test_underscore_option(self):
        sys.argv = [
            sys.argv[0], '--no-underscore-emphasis', '--dry-run', test_md]
        with patch(_builtin + '.print') as m:
            main()
        self.assertIn('__content__', m.call_args[0][0])
        self.assertNotIn('**content**', m.call_args[0][0])

    def test_anonymous_reference_option(self):
        sys.argv = [
            sys.argv[0], '--anonymous-references', '--dry-run', test_md]
        with patch(_builtin + '.print') as m:
            main()
        self.assertIn("`A link to GitHub <http://github.com/>`__",
                      m.call_args[0][0])

    def test_disable_inline_math(self):
        sys.argv = [
            sys.argv[0], '--disable-inline-math', '--dry-run', test_md]
        with patch(_builtin + '.print') as m:
            main()
        self.assertIn('``$E = mc^2$``', m.call_args[0][0])
        self.assertNotIn(':math:', m.call_args[0][0])
