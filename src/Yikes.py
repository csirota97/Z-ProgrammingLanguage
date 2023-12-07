import warnings

def compilationYikes(str):
    warnings.warn("BIG YIKES - compilation error\n{0}".format(str))

def runtimeYikes(str, line, line_number):
    warnings.warn("BIG YIKES - runtime error\n{0}\n{1} - {2}".format(str, line, line_number))
