#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path
from unittest import TestCase

from m2r import parse_from_file

curdir = path.dirname(path.abspath(__file__))


class TestConvert(TestCase):
    def test_a(self):
        fname = path.join(curdir, 'test.md')
        output = parse_from_file(fname)
        with open(path.join(curdir, 'test.rst')) as f:
            expected = f.read()
        self.assertEqual(output.strip(), expected.strip())
