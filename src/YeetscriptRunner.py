from BigYikes import compilationYikes as BYCompilation, runtimeYikes as BYRuntime
from Exceptions import OpenGiving, UnexpectedPeriod, UnknownValue, EvaluationError, BadNameError, UnknownFunction, MissingParametersError, UnterminatedQuoteError
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

def runner(filename=None, direct_input=None):
    if (direct_input == None):
        global code_lines, variables

        with open(filename or sys.argv[1], 'r') as file:
            code_lines = file.readlines()
    else:
        global variables
        code_lines = direct_input

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

    next_line_to_process = None
    for line_index, line in enumerate(code_lines):
        if next_line_to_process != None and next_line_to_process != line_index:
            continue
        elif next_line_to_process == line_index:
            next_line_to_process = None

        line_words = line.strip().split()
        line_number = line_index + 1
        if line_words == []:
            continue

        if any(isComment == '~~' for isComment in line_words):
            line_words = line_words[0:line_words.index('~~')]

        if 'giving' in line_words:
            callStack.append(len(callStack)+1)
        if 'period' in line_words:
            level_to_remove = callStack.pop()
            variables_copy = variables.copy()
            for variable in variables.items():
                if variable[1].callStackLevel == level_to_remove:
                    variables_copy.pop(variable[0])
            variables = variables_copy.copy()
                
        if 'slay' in line_words:
            slay_index = line_words.index('slay')
            function_not_found= False
            try:
                function_to_call = functions[line_words[slay_index+1]]
            except KeyError:
                function_not_found = True

            if function_not_found:
                BYRuntime(f"Function \"{line_words[slay_index+1]}\" has not been defined within the given scope.", line, line_number, UnknownFunction)

            joined_words = " ".join(line_words)
            line_words = combine_strings(line_words, line, line_number)

            if len(line_words[slay_index+2:]) < len(function_to_call.parameterNames):
                BYRuntime(f"Missing parameter for {function_to_call.name}.\n{len(line_words[slay_index+2:])} recieved/{len(function_to_call.parameterNames)} expected.", line, line_number, MissingParametersError)

            callStack.append(len(callStack)+1)
            for index, name in enumerate(function_to_call.parameterNames):
                variables[name] = Variable(name, line_words[slay_index+2+index], callStack[-1])

            runner(direct_input=function_to_call.steps)
            callStack.pop()

        if len(line_words) == 0:
            continue
        if line_words[0] in keywords:
            if line_words[0] == 'based' and line_words[2] == 'stan' and 'giving' not in line_words:
                '''
                Defining Variable
                '''
                if is_str_keyword(line_words[1]):
                    BYRuntime(f"Variable can not use a reserved keyword \"{line_words[1]}\" as a name", line, line_number, BadNameError)
                variables[line_words[1]] = Variable(line_words[1], process_value_from_code(line_words[3:], line_number, line), len(callStack))


            elif line_words[0] == 'based' and line_words[-1] == 'giving':
                '''
                Define Function
                '''
                if is_str_keyword(line_words[1]):
                    BYRuntime(f"Function can not use a reserved keyword \"{line_words[1]}\" as a name", line, line_number, BadNameError)
                paramKeyword = any_str_keyword(line_words[2:-1])
                if paramKeyword:
                    BYRuntime(f"Function can not use a reserved keyword \"{paramKeyword}\" as a parameter name", line, line_number, BadNameError)

                function_lines = code_lines[line_number-1:]
                function_call_indicator = 0
                for func_line_index, func_line in enumerate(function_lines):
                    if "giving" in func_line:
                        function_call_indicator += 1
                    if "period" in func_line:
                        function_call_indicator -= 1

                    if function_call_indicator == 0:
                        function_lines = function_lines[1:func_line_index]
                        next_line_to_process = func_line_index + line_index
                        break

                functions[line_words[1]] = Function(line_words[1], line_words[2:-1], function_lines )

            elif line_words[0] == 'spillTea':
                '''
                Print to console
                '''
                print(process_value_from_code(line_words[1:], line_number, line))


def is_number(string):
    '''
    Checks if string is a number
    '''
    try:
        return string == str(int(string)) or string == str(float(string))
    except ValueError:
        return False

def process_value_from_code(words, line_number, line):
    '''
    Process the value from the code
    '''
    joined_words = "".join(combine_strings(words, line, line_number)).strip()
    if joined_words == "":
        return ""
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
    except NameError:
        nameErr = True
    except ValueError:
        valErr = True

    if nameErr:
        BYRuntime("An unknown value could not be processed. Please check the spelling and scope of your code.", line, line_number, UnknownValue)
    if valErr:
        BYRuntime("The following line could not be evaluated", " ".join(words), line_number, EvaluationError)

def is_str_keyword(string):
    return string in keywords

def any_str_keyword(lst):
    if any(string in keywords for string in lst):
        for string in lst:
            if string in keywords:
                return string
    return False

def combine_strings(words, line, line_number):
    joined_words = " ".join(words)
    count = 0
    quote_indices = []
    for index, char in enumerate(joined_words):
        if char == '"':
            count += 1
            quote_indices.append(index)

    if count % 2 == 1:
        BYCompilation("Unterminated quote. Check for missing or extra quotes.", line, line_number, UnterminatedQuoteError)

    replacement_key = "%%%REPLACE%%%"
    strings = []
    for i in range(0, len(quote_indices), 2):
        strings.append(joined_words[quote_indices[i]:quote_indices[i+1]+1])

    for string in strings:
        joined_words = joined_words.replace(string, replacement_key)

    replacement_words = []
    replacement_words = [word if word != replacement_key else strings.pop(0) for word in joined_words.split(' ')]
 
    return replacement_words


if __name__ == '__main__':
    runner()
