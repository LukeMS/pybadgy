"""pybadgy: Script to generate custom shields.io-like badges."""
# -*- coding: utf-8 -*-

from __future__ import (print_function, division, absolute_import,
                        unicode_literals)

import argparse
import os
import pkg_resources
import re
import sys


__version__ = '0.1.0'

EXAMPLE = """example: pybadgy -f -o badge.svg -t coverage -v 100"""
DOXY_COVERAGE_PATTERN = "(?P<value>\d+)% ?API.+"
DEFAULT_COLOR = '#a4a61d'
COLORS = {
    'brightgreen': '#4c1',
    'green': '#97CA00',
    'yellowgreen': '#a4a61d',
    'yellow': '#dfb317',
    'orange': '#fe7d37',
    'red': '#e05d44',
    'lightgrey': '#9f9f9f',
}

COLOR_RANGES = [
    (95, 'brightgreen'),  # -r0 95 --range0 95
    (90, 'green'),        # -r1 90 --range0 90
    (75, 'yellowgreen'),  # -r2 75 --range0 75
    (60, 'yellow'),       # -r3 60 --range0 60
    (40, 'orange'),       # -r4 40 --range0 40
    (0, 'red'),
]


def get_color(total):
    """Return color for current coverage precent."""
    try:
        xtotal = int(total)
    except ValueError:
        return COLORS['lightgrey']
    for range_, color in COLOR_RANGES:
        if xtotal >= range_:
            return COLORS[color]


def get_badge(string="string", total=100, color=DEFAULT_COLOR):
    """Read the SVG template from the package and write custom fields.

    Return SVG as a string.
    """
    template_path = os.path.join('templates', 'flat.svg')
    template = pkg_resources.resource_string(__name__, template_path).decode(
        'utf8')
    return template.replace(
        '{{ total }}', total).replace(
        '{{ color }}', color).replace(
        '{{ string }}', string)


def get_badge2(label, value, color=DEFAULT_COLOR):
    """Read the SVG template from the package and write custom fields.

    Return SVG as a string.
    """
    template_path = os.path.join('templates', 'custom.svg')
    template = pkg_resources.resource_string(__name__, template_path).decode(
        'utf8')
    w0 = (len(label) - 1) * 8
    w1 = (len(value) + 1) * 8
    for (src, dest) in (
        ("{{w0+w1}}", w0 + w1),
        ("{{w0}}", w0),
        ("{{w1}}", w1),
        ("{{(w0+w1/2-1)*10}}", (w0 + (w1 / 2)) * 10),
        ("{{(((w0)/2)+1)*10}}", ((w0 / 2)) * 10),
        ("{{label}}", label),
        ("{{value}}", value),
        ("{{c1}}", "#555"),  # or #555
        ("{{c2}}", color),  # or #4c1
    ):
        template = template.replace(src, str(dest))
    return template


def parse_args(argv=None):
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser = argparse.ArgumentParser(epilog=EXAMPLE)
    parser.add_argument('-p', dest='plain_color', action='store_true',
                        help='Plain color mode. Standard green badge.')
    parser.add_argument('-f', dest='force', action='store_true',
                        help='Force overwrite image, use with -o key.')
    parser.add_argument('-q', dest='quiet', action='store_true',
                        help='Don\'t output any non-error messages.')
    parser.add_argument('-o', '--output', dest='filepath',
                        help='Save the file to the specified path.')
    parser.add_argument('-v', '--value', dest='value', type=int,
                        help='Show version.')
    parser.add_argument('-t', '--text', dest='text',
                        help='Text/label to write on the badge.')
    parser.add_argument('--doxy', dest='doxy',
                        help='Parse the given givendoxy-coverage file.')

    # If arguments have been passed in, use them.
    if argv:
        return parser.parse_args(argv)

    # Otherwise, just use sys.argv directly.
    else:
        return parser.parse_args()


def save_badge(badge, filepath, force=False):
    """Save badge to the specified path."""
    # Validate path (part 1)
    if filepath.endswith('/'):
        print('Error: Filepath may not be a directory.')
        sys.exit(1)

    # Get absolute filepath
    path = os.path.abspath(filepath)
    if not path.lower().endswith('.svg'):
        path += '.svg'

    # Validate path (part 2)
    if not force and os.path.exists(path):
        print('Error: "{}" already exists.'.format(path))
        sys.exit(1)

    # Write file
    with open(path, 'w') as f:
        f.write(badge)

    return path


def doxy_coverage_badge(filepath):
    """..."""
    with open(filepath) as f:
        linelist = f.readlines()

    text = "doxy-coverage"

    for l in reversed(linelist):
        match = re.match(DOXY_COVERAGE_PATTERN, l)
        if match:
            value = int(match.group('value'))
            break

    print("{}: {}%".format(text, value))

    return text, value


def main(argv=None):
    """Console scripts entry point."""
    args = parse_args(argv)

    # Show or save output
    if args.doxy:
        text, value = doxy_coverage_badge(args.doxy)
        value = '{0:.0f}'.format(value)
        color = DEFAULT_COLOR if args.plain_color else get_color(value)
        percent = '{0}%'.format(value)
        badge = get_badge2(text, percent, color)
    else:
        text = args.text
        total = '{0:.0f}'.format(args.value)
        color = DEFAULT_COLOR if args.plain_color else get_color(total)
        badge = get_badge(text, total, color)

    # Show or save output
    if args.filepath:
        path = save_badge(badge, args.filepath, args.force)
        if not args.quiet:
            print('Saved badge to {}'.format(path))
    else:
        print(badge, end='')


if __name__ == "__main__":
    main()
