#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path
import subprocess
from livereload import Server, shell

docsdir = path.dirname(path.abspath(__file__))
builddir = path.join(docsdir, '_build')

subprocess.run(['make', 'clean'])
subprocess.run(['make', 'html'])
cmd = shell(['sphinx-build', '-b', 'html', '-E',
             '-d', path.join(builddir, 'doctrees'),
             docsdir, path.join(builddir, 'html')])

server = Server()
server.watch('*.py', cmd)
server.watch('../*.py', cmd)
server.watch('*.md', cmd)
server.watch('../*.md', cmd)
server.watch('_static/*.css', cmd)
server.watch('_templates/*.html', cmd)

server.serve(port=8889, root='_build/html', debug=True, restart_delay=1)
