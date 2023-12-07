from BigYikes import compilationYikes as BYCompilation, runtimeYikes as BYRuntime
valid_name_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_'

class Variable:
    def __init__(self, name, value, callStackLevel):
        if not name[0].isalpha:
            BYCompilation("{0} is an invalid variable name. Variable names must begin with a letter.".format(name))
        for char in name:
            if char not in valid_name_chars:
                BYCompilation("{0} is an invalid variable name. Variable names must contain only letters, numbers, and underscores.".format(name))

        self.name = name
        self.value = value
        self.callStackLevel = callStackLevel

    