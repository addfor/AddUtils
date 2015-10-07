# The MIT License (MIT)
# 
# Copyright (c) 2015 addfor s.r.l.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
from subprocess import Popen, PIPE
import json

from pip.commands import install


def _call_conda(extra_args):
    args = ['conda'] + extra_args
    try:
        p = Popen(args, stdout=PIPE, stderr=PIPE)
    except OSError:
        raise Exception("could not invoke %r\n" % args)
    return p.communicate()[0].decode('utf-8')


def search_outdated():
    packages = json.loads(_call_conda(['search', '-o', '--json']))
    return [p for p in packages if p!='python' and packages[p]]


def update_all(retry=10):
    i = 0
    while i<retry:
        to_update = search_outdated()
        if to_update:
            for package in to_update:
                try:
                    print _call_conda(['update', '-y', package])
                except:
                    print "Error updating %s, please try manually." % package 
                i += 1
        else:
            return


def install_from_pip(distribution_name):
    command = install.InstallCommand()
    opt, args = command.parser.parse_args()
    try:
        r_set = command.run(opt, [distribution_name])
        r_set = command.run(opt, [distribution_name])
    except Exception as e:
        print e
        print "Error installing %s, please try manually" % distribution_name


if __name__ == "__main__":
    update_all()
    install_from_pip('fake-factory')
    install_from_pip('liac-arff')
    print _call_conda(['install', 'seaborn'])
    
