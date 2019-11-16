import sys

sys.path.insert(0, 'lib')

from lib import teek


def buttons(frame, l, column_limit=3):
    """
    Generates and places common buttons

    :param column_limit:
    :param frame:
    :param l:
    :return:
    """
    tk_elements = {}
    r = 0
    c = 0
    for i in l:
        b = teek.Button(frame, i)
        b.grid(row=r, column=c)
        tk_elements[i] = b
        c += 1
        if c == column_limit:
            c = 0
            r += 1
    return tk_elements


w = teek.Window("RAMCalc")
w.on_delete_window.connect(teek.quit)
e = teek.Text(w, height=1)
e.grid(row=0, column=0, columnspan=3)

mf = teek.Frame(w)
mf.grid(row=1, column=0, rowspan=2)
math_functions = ["sin", "cos", "tan", "sqrt", "log"]
buttons(mf, math_functions)

nf = teek.Frame(w)
nf.grid(row=1, column=1)
buttons(nf, list(range(1, 10)) + ["(", 0, ")"])

operators = ["+", "-", "*", "/"]
of = teek.Frame(w)
of.grid(row=1, column=2, rowspan=2)
buttons(of, operators, column_limit=1)
teek.run()
