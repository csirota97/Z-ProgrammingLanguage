from BigYikes import compilationYikes as BYCompilation, runtimeYikes as BYRuntime
from Exceptions import OpenGiving, UnexpectedPeriod
import sys
import warnings
from Yikes import compilationYikes as YCompilation, runtimeYikes as YRuntime


from Function import Function
from Variable import Variable
from YS_Keywords import keywords

functions = {}
variables = {}
callStack = []

code_lines = None

def runner(filename=None):
    global code_lines, variables
    with open(filename or sys.argv[1], 'r') as file:
        code_lines = file.readlines()

    giving_count = 0
    period_count = 0
    for line in code_lines:
        if "giving" in line:
            giving_count += 1

        if "period" in line:
            period_count += 1
            
    if (giving_count > period_count):
        BYCompilation(OpenGiving, "Open Giving-Period. Check for missing period(s).")
    elif (giving_count < period_count):
        BYCompilation(UnexpectedPeriod, "Unexpected period")

    for line_index, line in enumerate(code_lines):
        line_words = line.strip().split()
        line_number = line_index + 1
        if line_words == []:
            continue

        if 'giving' in line_words:
            callStack.append(len(callStack)+1)
        if 'period' in line_words:
            level_to_remove = callStack.pop()
            variables_copy = variables.copy()
            for variable in variables.items():
                if variable[1].callStackLevel == level_to_remove:
                    variables_copy.pop(variable[0])
            variables = variables_copy.copy()
                

        if line_words[0] in keywords:
            if line_words[0] == 'based' and line_words[2] == 'stan':
                variables[line_words[1]] = Variable(line_words[1], process_value_from_code(line_words[3:], line_number), len(callStack))
            if line_words[0] == 'spillTea':
                print(process_value_from_code(line_words[1:], line_number))


def is_number(string):
    '''
    Checks if string is a number
    '''
    try:
        return string == str(int(string)) or string == str(float(string))
    except ValueError:
        return False

def process_value_from_code(words, line_number):
    '''
    Process the value from the code
    '''
    joined_words = "".join(words).strip()
    try:
        if (joined_words[0] == '"' and joined_words[-1] == '"') or (joined_words[0] == "'" and joined_words[-1] == "'"):
            return joined_words[1:-1]
        elif joined_words == str(float(joined_words)):
            return float(joined_words)
        elif joined_words == str(int(joined_words)):
            return int(joined_words)
        return variables[joined_words].value
    except ValueError:
        try:
            return variables[joined_words].value
        except KeyError:
            pass
    except KeyError:
        pass


    if all((is_number(word) or word in "+-/*()") for word in words):
        return eval(" ".join(words))

    eval_words = []
    for word in words:
        try:
            eval_words.append(variables[word].value)
        except KeyError:
            eval_words.append(word)

    try:
        return eval(" ".join([str(word) for word in eval_words]))
    except ValueError:
        BYRuntime("The following line could not be evaluated", " ".join(words), line_number)

if __name__ == '__main__':
    runner()
