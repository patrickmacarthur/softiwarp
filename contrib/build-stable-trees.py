#!/usr/bin/python3
# Usage: build-stable-trees.py
#
# Copyright (c) 2017, University of New Hampshire
#
# This software is available to you under a choice of one of two
# licenses.  You may choose to be licensed under the terms of the GNU
# General Public License (GPL) Version 2, available from the file
# COPYING in the main directory of this source tree, or the
# BSD license below:
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#   - Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#   - Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#   - Neither the name of IBM nor the names of its contributors may be
#     used to endorse or promote products derived from this software without
#     specific prior written permission.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Builds softiwarp against each Linux kernel stable tree.

For every long-term kernel release, build the corresponding kernel tree.
This script was written for Ubuntu 16.10 and will need to be adjusted
for other Linux distributions.

This script is based off the list of long-term releases at:

    https://www.kernel.org/category/releases.html

For this script to work, you will need to have a git clone of the Linux
kernel at ~/src/kernel.org/linux.  Then (assuming at least git 2.5), you
can create worktrees for each stable release as follows:

    git remote add stable \
        git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git
    git fetch --all
    for i in 4.4 4.1 3.18 3.16 3.12 3.10 3.4 3.2; do
        git branch -t linux-${i}.y stable/linux-${i}.y
        git worktree add ../linux-${i}.y linux-${i}.y
        make -C ../linux-${i}.y mrproper defconfig modules_prepare
    done

You will then have a work tree for each stable kernel release at
~/src/kernel.org/linux-X.Y.y for each X.Y long-term release.
"""

import os
import os.path
import subprocess
import sys

# Adjust this if you keep your kernel trees elsewhere
kernels_dir = os.path.join(os.environ['HOME'], 'src/kernel.org')

# Adjust this as the set of long-term trees is changed
trees = [
    {'name': "linux-3.2.y", 'cc': "gcc-4.9"},
    {'name': "linux-3.4.y", 'cc': "gcc-4.9"},
    {'name': "linux-3.10.y", 'cc': "gcc"},
    {'name': "linux-3.12.y", 'cc': "gcc"},
    {'name': "linux-3.16.y", 'cc': "gcc"},
    {'name': "linux-3.18.y", 'cc': "gcc"},
    {'name': "linux-4.1.y", 'cc': "gcc"},
    {'name': "linux-4.4.y", 'cc': "gcc"},
    {'name': "linux-4.9.y", 'cc': "gcc"}
]

for tree in trees:
    name = tree['name']
    subprocess.call(['git', 'clean', '-x', '-f', '-d'])
    try:
        src_path = os.path.join(kernels_dir, name)
        subprocess.check_call(['make', 'CC={0}'.format(tree['cc']),
                               'EXTRA_CFLAGS=-fno-pie -fno-stack-protector',
                               'LINUX_SRC_PATH={0}'.format(src_path),
                               'modules'])
        print('+++ build with stable kernel {0}: SUCCESS +++'.format(name))
    except subprocess.CalledProcessError:
        print('*** build with stable kernel {0}: FAILURE ***'.format(name))
        sys.exit(1)
