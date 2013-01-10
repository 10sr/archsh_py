#!/usr/bin/env python3

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
DEF = -1

_ESC_CODE = "\033"
_CODE_BASE = "\033" + "[{}m"
def colored(s, fg=DEF, bg=DEF,
            bold=False, italic=False, underline=False, inverse=False,
            strikethrough=False):

    code = []

    if bold:
        code.append("1")

    if italic:
        code.append("3")

    if underline:
        code.append("4")

    if inverse:
        code.append("7")

    if strikethrough:
        code.append("9")

    if fg != DEF:
        code.append("3" + str(fg))

    if bg != DEF:
        code.append("4" + str(bg))

    codestr = ";".join(code)

    return _CODE_BASE.format(codestr) + s + _CODE_BASE.format(0)

if __name__ == "__main__":
    c1 = colored("red str", fg=RED, underline=True)
    c2 = colored("blue with yellow bg", fg=BLUE, bg=YELLOW, bold=True)
    print(c1 + " normal str")
    print(c2)
