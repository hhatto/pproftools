#!/usr/bin/env python
import sys
import re
import argparse

RE_STARTLINE = re.compile("[0-9]? @ 0x")
RE_STACKINFO_LINE = re.compile("#\t0x")

GOROUTINE_NUM_COLOR = 11
COLOR_LEVELS = [196, 202, 208, 214, 248, 250, 252]


def _main(lines, opts):
    is_first = True
    stacks = []
    one_stackinfo = []
    goroutine_num = 0

    # parse
    level = 0
    for line in lines:
        if RE_STACKINFO_LINE.match(line):
            if opts.color:
                line = "\x1b[;38;5;%03dm%s\x1b[;39m" % (COLOR_LEVELS[level], line)
                if len(COLOR_LEVELS)-1 > level:
                    level += 1
            one_stackinfo.append(line)
        if RE_STARTLINE.search(line):
            if is_first:
                is_first = False
            else:
                stacks.append({
                    "num": goroutine_num,
                    "info": "".join([stack for stack in one_stackinfo])
                })
                one_stackinfo = []
                level = 0
            goroutine_num = int(line.split()[0])
            if opts.color:
                tmp = line.split()
                line = "\x1b[;38;5;%03dm%s\x1b[;39m " % (GOROUTINE_NUM_COLOR, tmp[0])
                line += " ".join(tmp[1:])
                line += "\n"
            one_stackinfo.append(line)

    # care for last info
    stacks.append({
        "num": goroutine_num,
        "info": "".join([stack for stack in one_stackinfo])
    })

    # sort and output
    sorted_stacks = sorted(stacks, key=lambda i: i["num"], reverse=not opts.reverse)
    for stackinfo in sorted_stacks:
        print("*" * 50)
        print("%s" % stackinfo["info"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--color', action='store_true', help='color print')
    parser.add_argument('-r', '--reverse', action='store_true', help='sort reverse by num goroutine')
    parser.add_argument('file', nargs='?', type=argparse.FileType('r+'),
                        help="pprof's goroutine dump text")
    args = parser.parse_args()
    if args.file is None:
        _main(sys.stdin, args)
    else:
        _main(args.file, args)
    return 0

if __name__ == '__main__':
    sys.exit(main())
