#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Doit task definitions."""

DOIT_CONFIG = {
    'default_tasks': [
        'flake8',
        'docs',
    ],
    'continue': True,
    'verbosity': 1,
    'num_process': 2,
    'par_type': 'thread',
}


def task_flake8():
    return {
        'actions': ['flake8 m2r tests'],
    }


def task_docs():
    return {
        'actions': ['sphinx-build -q -W -E -n -b html docs docs/_build/html'],
    }
