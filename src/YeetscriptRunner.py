import BigYikes
import Function
import sys
import Variable
import warnings
import Yikes

from YS_Keywords import keywords

functions = {}
variables = {}
callStack = []

code_lines = None

def runner():
    with open(sys.argv[1], 'r') as file:
        code_lines = file.readlines()

    giving_count = 0
    period_count = 0
    for line in code_lines:
        if "giving" in line:
            giving_count += 1

        if "period" in line:
            period_count += 1
            
    if (giving_count > period_count):
        BigYikes.compilationYikes("Open Giving-Period. Check for missing period(s).")
    elif (giving_count < period_count):
        BigYikes.compilationYikes("Unexpected period")

    for line_index, line in enumerate(code_lines):
        line_words = line.strip().split()
        line_number = line_index + 1
        if line_words == []:
            continue

        if line_words[0] in keywords:
            if line_words[0] == 'based' and line_words[2] == 'stan':
                variables.append(Variable(line_words[1], line_number))


def isNumber(str):
    try:
        return joined_words == str(int(joined_words)) or joined_words == str(float(joined_words))
    except ValueError:
        return False

def processValueFromCode(words, line_number):
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
        return variables[joined_words].value
    except KeyError:
        pass


    if all(isNumber(word) or word in "+-/*()" for word in words):
        return eval()

    eval_words = []
    for word in words:
        try:
            eval_words.push(variables[word].value)
        except KeyError:
            eval_words.push(word)

    try:
        return eval(" ".join(eval_words))
    except ValueError:
        BigYikes.runtimeYikes("The following line could not be evaluated", " ".join(words), line_number)

if __name__ == '__main__':
    runner()