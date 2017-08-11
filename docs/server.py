#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path
import subprocess

from livereload import Server

docsdir = path.dirname(path.abspath(__file__))
builddir = path.join(docsdir, '_build')
build_cmd = [
    'sphinx-build', '-b', 'html', '-E', '-q',
    '-d', path.join(builddir, 'doctrees'),
    docsdir, path.join(builddir, 'html'),
]


def cmd() -> None:
    print('=== Sphinx Build Start ===')
    subprocess.run(build_cmd, cwd=docsdir)
    print('=== Sphinx Build done ===')


def docs(p: str) -> str:
    return path.join(docsdir, p)


# subprocess.run(['make', 'clean'], cwd=docsdir)
cmd()  # build once
server = Server()

server.watch(docs('*.py'), cmd)
server.watch(docs('../*.py'), cmd)
server.watch(docs('*.md'), cmd)
server.watch(docs('../*.md'), cmd)
server.watch(docs('_static/*.css'), cmd)
server.watch(docs('_templates/*.html'), cmd)

server.serve(port=8889, root=docs('_build/html'), debug=True, restart_delay=1)
