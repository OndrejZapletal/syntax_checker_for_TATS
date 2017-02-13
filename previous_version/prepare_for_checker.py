# Author: Ondrej Zapletal
# Date: 2016-01-21
# Description:
import re
import ipdb


def analyze_identifier_reference(word):
    """Function estimates all necessary states about identifier and triggers
    Error or Warnings.

    @param word: identifier or operator
    @return: TODO: value of identifier

    """
    print('analyze_identifier_reference: "{0}"'.format(word))
    # if word == " and ":
    #     ipdb.set_trace()  # #BREAKPOINT#
    if word == VALUE:
        return VALUE

    elif word == NULL:
        return NULL

    else:
        if ' ' not in word:
            word = re.escape(word)

        if word.lower() in ALL_OPERATORS:
            return OPERATOR
        else:
            return VALUE


def return_value_of_expression(arg1, oper, arg2):
    """Function takes two operands and operator to compute result of expression

    @param arg1 - operand left
    @param oper - operator
    @param arg2 - operand right
    @return: result of operator operation

    """
    print('return_value_of_expression: "{0}", "{1}", "{2}"'.format(
        arg1, oper, arg2))
    if oper is OPERATOR:
        if arg1 is VALUE and arg2 is VALUE:
            return VALUE
        elif arg1 is VALUE and arg2 is NULL:
            return NULL
        elif arg1 is NULL and arg2 is VALUE:
            return NULL
        elif arg1 is NULL and arg2 is NULL:
            return NULL
        else:
            ipdb.set_trace()  # #BREAKPOINT#
    else:
        return INVALID


def evaluate_expression(string):
    """Function evaluates expression that is present in input string.

    @param string - contains expression
    @return: evaluated result of expression
        - #VALUE# - proper value
        - #NULL# - no return value (for example procedure call without return
        value instead of function call)
        - #MISSING_OPERATOR# - two values (identifiers of functions) are not
        correctly separated by operand (either operand is missing entirely or
        it has improper format)
        - #INVALID# - TODO
    """
    # print('evaluate_expression: "{0}"'.format(string))
    evaluation_string = \
        r'\s*({0}|{1}|{2})\s*{3}\s*({0}|{1}|{2})(.*)'.format(
            VALUE, NULL, IDENTIFIER, EVALUATING_OPERATORS)
    single_value_string = \
        r'^\s*({0}|{1}|{2})\s*$'.format(
            VALUE, NULL, IDENTIFIER)
    missing_operator_string = \
        r'\s*({0}|{1}|\b\w+\b)\s*({0}|{1}|\b\w+\b)(.*)'.format(
            VALUE, NULL)
    contains_invalid_string = r'\s*({0})'.format(INVALID)

    single_value_regex = re.compile(single_value_string, re.IGNORECASE)
    evaluation_regex = re.compile(evaluation_string, re.IGNORECASE)
    missing_operator_regex = re.compile(missing_operator_string, re.IGNORECASE)
    contains_invalid_regex = re.compile(contains_invalid_string, re.IGNORECASE)
    if string == "":
        return ""
    elif single_value_regex.match(string):
        single_value_match = single_value_regex.match(string)
        return analyze_identifier_reference(single_value_match.group(1))

    elif evaluation_regex.match(string):
        evaluation_match = evaluation_regex.match(string)
        print('"{0}", "{1}", "{2}"'.format(
            evaluation_match.group(1), evaluation_match.group(4),
            evaluation_match.group(5)))
        arg1 = analyze_identifier_reference(evaluation_match.group(1))
        if evaluation_match.group(4):
            operator = analyze_identifier_reference(evaluation_match.group(4))
        else:
            operator = ""
        arg2 = analyze_identifier_reference(evaluation_match.group(5))
        string = return_value_of_expression(arg1, operator, arg2)

        if evaluation_match.group(8):
            return evaluate_expression(string + evaluation_match.group(8))
        else:
            return string
    elif contains_invalid_regex.match(string):
        return INVALID
    elif missing_operator_regex.match(string):
        return MISSING_OPERATOR
    else:
        ipdb.set_trace()  # #BREAKPOINT#


def process_inner_function_prototype(
        function_string, position, name_space, function_name=""):
    """TODO: Docstring for process_inner_function_prototype.

    :function_string: TODO
    :position: TODO
    :name_space: TODO
    :functin_name: TODO
    :returns: TODO

    """
    print('process_inner_function_prototype: "{0}"'.format(function_string))
    list_of_parameters = []
    parameters_correct = True

    fun_prot_match = re.search(
            r'((\b[a-zA-Z]\w+\b)\.)?(\b[a-zA-Z]\w+\b)\s*\(([^()]*)\)',
            function_string)

    object_name = ""
    if fun_prot_match.group(2):
        object_name = fun_prot_match.group(2)
    fun_name = fun_prot_match.group(3)
    parameters = fun_prot_match.group(4)

    for parameter in parameters.split(","):
        evaluated_parameter = evaluate_expression(parameter)
        if evaluated_parameter == VALUE:
            list_of_parameters.append(VALUE)

        elif evaluated_parameter == NULL:
            parameters_correct = False
            list_of_parameters.append(NULL)

        elif evaluated_parameter == INVALID:
            parameters_correct = False
            list_of_parameters.append(INVALID)

        elif evaluated_parameter == MISSING_OPERATOR:
            parameters_correct = False
            list_of_parameters.append(MISSING_OPERATOR)

    if parameters_correct:
        if object_name != "":
            result = analyze_method(object_name, fun_name, list_of_parameters)
        else:
            result = analyze_function(fun_name, list_of_parameters)
        return result
    else:
        return INVALID


def analyze_method(object_name, method_name, list_of_parameters):
    """Anlyzes method call defined object_name and method_name.
    list_of_parameters is used to determined if the function definition is
    corrsponding to number of parameters that this function is called with.

    @param object_name TODO
    @param method_name TODO
    @param list_of_parameters TODO
    @return:
        - #VALUE# - normal return
        - #NULL# - no return value (in case of Sub)
        - #INVALID# - wrong function paramters
    """
    return VALUE


def analyze_function(fun_name, list_of_parameters):
    """Anlyzes function call defined by function name. list_of_parameters is
    used to determined if the function definition is corrsponding to number of
    parameters that this function is called with.

    @param fun_name TODO
    @param list_of_parameters TODO
    @return:
        - #VALUE# - normal return
        - #NULL# - no return value (in case of Sub)
        - #INVALID# - wrong function paramters
    """
    return VALUE


def analyze_and_evaluate_reference_side(
        function_string, position, name_space, function_name=""):
    """ Function is called on string that might contain function call. In case
    that regex which is designed to fined most inner brace in expression finds
    pattern that describes function call it is analyzed by function
    process_inner_function_prototype.

    :function_string: TODO
    :position: TODO
    :name_space: TODO
    :function_name: TODO
    :returns: TODO
    """
    print('analyze_and_evaluate_reference_side: "{0}"'.format(function_string))
    inner_fun_regx = re.compile(
        r'(((\b[a-zA-Z]\w+\b)\.)?((\b[a-zA-Z]\w+\b)\s*\(([^()]*)\)))',
        re.IGNORECASE)

    while inner_fun_regx.search(function_string):
        m = inner_fun_regx.search(function_string)
        begin = m.start(1)
        end = m.end(1)
        function_result = process_inner_function_prototype(
                m.group(1), position + begin, 0)
        try:
            function_string = function_string[:begin] + function_result + \
                function_string[end:]
        except TypeError:
            ipdb.set_trace()  # #BREAKPOINT#
            pass

    if re.search('[(]', function_string):
        return MISS_OPN
    elif re.search('[)]', function_string):
        return MISS_CLS

    return evaluate_expression(function_string)


ARITHMETIC_OPERATORS = ['\*', '\/', '\+', '-', ' mod ', '\&', r'\\', '\^']
ARITHMETIC_OPERATORS_NOSPACE = \
        ['\*', '\/', '\+', '-', ' mod ', '\&', r'\\', '\^']

ASSIGNMENT_OPERATORS = ['=']

COMPARISON_OPERATORS = ['=', '<>', '<', '>', '<=', '>=', ' is ']

CONCATENATION_OPERATORS = ['\&', '\+']

LOGICAL_OPERATORS = [' xor ', ' or ', ' and ', ' imp ', ' eqv ', ' not ']
LOGICAL_OPERATORS_NOSPACE = ['xor', 'or', 'and', 'imp', 'eqv', 'not']

IDENTIFIER = '(".*?"|&\w+|\w+|[+-]?\d+(\.\d+)?)'

ALL_OPERATORS = ARITHMETIC_OPERATORS + ASSIGNMENT_OPERATORS + \
    COMPARISON_OPERATORS + CONCATENATION_OPERATORS + LOGICAL_OPERATORS

EVALUATING_OPERATORS = "({0})".format('|'.join(ALL_OPERATORS))

MISS_CLS = "#MISSING_CLOSING#"
MISS_OPN = "#MISSING_OPENING#"
VALUE = "#VALUE#"
NULL = "#NULL#"
OPERATOR = "#OPERATOR#"
MISSING_OPERATOR = "#MISSING_OPERATOR#"
INVALID = "#INVALID#"

test_string13 = "fun1(arg1 + arg2 + argr + func3())"
test_string16 = \
    '(InStr(Result,"LINE 2 OF MESSAGE") > 0 )  And ( (InStr(' \
    'Result,"LINE 7 OF MESSAGE") > 0 ) ) And ( (InStr(Result,' \
    '"MESSAGE INCOMPLETE") > 0 ) )'

analyze_and_evaluate_reference_side(test_string16, 0, 0)
