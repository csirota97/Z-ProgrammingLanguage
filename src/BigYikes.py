def compilationYikes(exception, str):
    raise exception("BIG YIKES - compilation error\n{0}".format(str))

def runtimeYikes(str, line, line_number, exception=None):
    exception_to_use = exception
    if exception == None:
        exception_to_use = Exception
    raise exception_to_use("BIG YIKES - runtime error\n{0}\nLn-{1} >{2}".format(str, line_number, line))
