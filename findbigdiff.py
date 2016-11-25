#!/usr/bin/env python
import sys
import re
import argparse

RE_START_LINE = re.compile("ROUTINE ========================")
RE_TOTAL_DIFF_PERCENT_LINE = re.compile("(\-?[0-9]+\.[0-9]+?)% of Total")

GOROUTINE_NUM_COLOR = 11
COLOR_LEVELS = [196, 202, 208, 214, 248, 250, 252]


def _main(lines, opts):
    is_first = True
    is_first_line = True
    stacks = []
    one_stackinfo = []
    percent = 0.0

    # parse
    for line in lines:
        if is_first_line:
            is_first_line = False
            continue
        if RE_START_LINE.search(line):
            if is_first:
                is_first = False
            else:
                stacks.append({
                    "percent": percent,
                    "info": "".join([stack for stack in one_stackinfo])
                })
                one_stackinfo = []
                percent = 0.0
        elif RE_TOTAL_DIFF_PERCENT_LINE.search(line):
            s = RE_TOTAL_DIFF_PERCENT_LINE.search(line)
            percent = float(s.group(1))
        one_stackinfo.append(line)

    # care for last info
    stacks.append({
        "percent": percent,
        "info": "".join([stack for stack in one_stackinfo])
    })

    # sort and output
    sorted_stacks = sorted(stacks, key=lambda i: i["percent"], reverse=not opts.reverse)
    for stackinfo in sorted_stacks:
        if stackinfo["percent"] < opts.threshold:
            continue
        print("%s" % stackinfo["info"])


def main():
    parser = argparse.ArgumentParser(description="""tool's usage:
     $ go tool pprof -list=. -base BASE.PPROF.DUMP BIANRY PPROF.DUMP > tmp.list
     $ python findbigdiff.py tmp.list""")
    parser.add_argument('-t', '--threshold', type=float, default=10.0, help='difference threshold. (default: 10.0[%%])')
    parser.add_argument('-r', '--reverse', action='store_true', help='sort reverse by difference percent')
    parser.add_argument('file', nargs='?', type=argparse.FileType('r+'),
                        help="pprof's difference list text")

    args = parser.parse_args()
    if args.file is None:
        _main(sys.stdin, args)
    else:
        _main(args.file, args)
    return 0

if __name__ == '__main__':
    sys.exit(main())
