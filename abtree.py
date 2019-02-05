import sys
import re
import numpy as np

class NotInAlphabet(Exception):
    """Raised when string uses characters not in alphabet"""

class CannotConstruct(Exception):
    """Raised when string cannot be made by the rules"""

class WrongArguments(Exception):
    """Should pass string of a's and b's then file to write to"""

class ruleTree:
    def __init__(self,val,childList,rule):
        self.children = childList
        self.rule = rule
        self.val = val
    def __str__(self):
        return self.val
    def __repr__(self):
        return self.val

def solve(s):
    if s == "":
        return ruleTree("\\epsilon",[],0)
    elif s[0] == "a" and s[-1] == "b":
        return ruleTree(s,[solve(s[1:-1])],1)
    elif s[0] == "b" and s[-1] == "a":
        return ruleTree(s,[solve(s[1:-1])],2)
    count = 0
    for i in range(len(s)):
        if count == 0 and i != 0:
            return ruleTree(s,[solve(s[:i]),solve(s[i:])],3)
        if s[i] == "a":
            count += 1
        else:
            count -= 1
    raise CannotConstruct


def formString(t):
    if t.children == []:
        return t.val
    else:
        return "\\cfrac{"+" \\ \\ ".join([formString(s) for s in t.children])+"}{"+t.val+"}"

def makeFile(s,name):
    with open(name,"w") as f:
        f.write("\\documentclass{article}\n \\usepackage{amsmath} \n \\begin{document} \n")
        f.write("$"+formString(s)+"$\n \\end{document}")

#ls = ['a' for i in range(40)] + ['b' for i in range(40)]
#x = solve("".join(np.random.permutation(ls)))
#makeFile(x,"ab.tex")

#Rules: 0 = axiom, 1 = add aub, 2 = add bua, 3 = add uv
if len(sys.argv) != 3:
    raise WrongArguments
base = sys.argv[1]
if re.search("[ab]*",base) != base:
    raise NotInAlphabet
if len(s) % 2 == 1:
    raise CannotConstruct
makeFile(solve(base),sys.argv[2])
