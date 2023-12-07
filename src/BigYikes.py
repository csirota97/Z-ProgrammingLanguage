def compilationYikes(exception, str):
    raise exception("BIG YIKES - compilation error\n{0}".format(str))

def runtimeYikes(str, line, line_number):
    raise Exception("BIG YIKES - runtime error\n{0}\n{1} - {2}".format(str, line, line_number))
