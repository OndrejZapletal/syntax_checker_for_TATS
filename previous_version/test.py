# Author: Ondrej Zapletal
# Date: 2016-01-21
# Description:
import re
import ipdb
# import sys


# def process_paramter(parameter, level):
#     # print(level*'\t'+"parameter beeing processed is {0}".format(parameter))
#     pass


# def analyze_function_params(function_name, function_parameters):
#     # print('\t\t\t\tAnalyzing function "{0}" with parameters "{1}"'.format(
#         # function_name, function_parameters))
#     return VALUE

# def parse_outer_brace(
#         whole_outer_function, position, name_space, functin_name=""):
#     fun_prot_regx = re.compile(
#         r'(((\b[a-zA-Z]\w+\b)\.)?(\b[a-zA-Z]\w+\b)\s*\((.*)\))',
# re.IGNORECASE)
#     fun_incorrect_regx = re.compile(
#         r'((\b[a-zA-Z]\w+\b)\.)?(\b[a-zA-Z]\w+\b)\s*\(', re.IGNORECASE)
#     if fun_prot_regx.search(whole_outer_function):
#         outer_function_name = fun_prot_regx.search(
#                 whole_outer_function).group(4)
#         inner_fun_params =
# fun_prot_regx.search(whole_outer_function).group(5)
#         m1 = fun_prot_regx.search(whole_outer_function)

#         if fun_prot_regx.search(inner_fun_params):
#             m = fun_prot_regx.search(inner_fun_params)
#             inner_fun_string =
# fun_prot_regx.search(inner_fun_params).group(1)
#             begin = m.start(1)
#             end = begin + len(inner_fun_string)
#             function_return = parse_outer_brace(
#                     inner_fun_string, position + m1.end(4) + begin + 1,
#                     name_space)
#             if function_return == "#MISSING#BRACKET#":
#                 return "#MISSING#BRACKET#"

#             inner_fun_params = inner_fun_params[:begin] + function_return + \
#                 inner_fun_params[end:]

#             result = analyze_function_params(
#                 outer_function_name, inner_fun_params)
#             return result
#         elif fun_incorrect_regx.search(inner_fun_params):
#             return "#MISSING#BRACKET#"

#         else:

#             return analyze_function_params(
#                     outer_function_name, inner_fun_params)
#     else:
#         ipdb.set_trace()  # #BREAKPOINT#
#         return VALUE


# def analyze_function(self, function_name, parameters):
#     pass


# def analyze_mehtod(self, object_name, method_name, parameters):
#     pass


# def evaluate_expression2(string):
#     good_string = r'\s*{0}\s*{1}\s*{0}(.*)'.format(
#             VALUE, EVALUATING_OPERATORS)
#     half_bad_string = r'\s*({0}\s*{2}\s*{1})|({1}\s*{2}\s*{0})(.*)'.format(
#             NULL, VALUE, EVALUATING_OPERATORS)
#     bad_string = r'\s*{0}\s*{1}\s*{0}(.*)'.format(
#             NULL, EVALUATING_OPERATORS)

#     result = ""
#     good_regex = re.compile(good_string, re.IGNORECASE)
#     half_bad_regex = re.compile(half_bad_string, re.IGNORECASE)
#     bad_regex = re.compile(bad_string, re.IGNORECASE)

#     if good_regex.match(string):
#         m = good_regex.match(string)
#         if m.group(2):
#             string = VALUE + m.group(2)
#             result = evaluate_expression2(string)
#         else:
#             return VALUE
#     elif half_bad_regex.match(string):
#         m = half_bad_regex.match(string)
#         if m.group(5):
#             string = NULL + m.group(5)
#             result = evaluate_expression2(string)
#         else:
#             return NULL
#     elif bad_regex.match(string):
#         m = bad_regex.match(string)
#         if m.group(2):
#             string = NULL + m.group(2)
#             result = evaluate_expression2(string)
#         else:
#             return NULL
#     elif re.match(r'\s*' + NULL + r'\s*$', string):
#         return NULL
#     elif re.match(r'\s*' + VALUE + r'\s*$', string):
#         return VALUE

#     return result


def analyze_identifier(word):
    print('analyze_identifier: "{0}"'.format(word))
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


def compute_expression(arg1, oper, arg2):
    print('compute_expression: "{0}", "{1}", "{2}"'.format(arg1, oper, arg2))
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
    print('evaluate_expression: "{0}"'.format(string))
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
        return analyze_identifier(single_value_match.group(1))

    elif evaluation_regex.match(string):
        evaluation_match = evaluation_regex.match(string)
        print('"{0}", "{1}", "{2}"'.format(
            evaluation_match.group(1), evaluation_match.group(4),
            evaluation_match.group(5)))
        arg1 = analyze_identifier(evaluation_match.group(1))
        if evaluation_match.group(4):
            operator = analyze_identifier(evaluation_match.group(4))
        else:
            operator = ""
        arg2 = analyze_identifier(evaluation_match.group(5))
        string = compute_expression(arg1, operator, arg2)

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


def process_inner(function_string, position, name_space, function_name=""):
    """TODO: Docstring for process_inner.

    :function_string: TODO
    :position: TODO
    :name_space: TODO
    :functin_name: TODO
    :returns: TODO

    """
    print('process_inner: "{0}"'.format(function_string))
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


def analyze_method(object_name, fun_name, list_of_parameters):
    return VALUE


def analyze_function(fun_name, list_of_parameters):
    return VALUE


def parse_inner_brace(function_string, position, name_space, function_name=""):
    """ Function is called on string that might contain function call. In case
    that regex which is designed to fined most inner brace in expression finds
    pattern that describes function call it is analyzed by function
    process_inner.

    :function_string: TODO
    :position: TODO
    :name_space: TODO
    :function_name: TODO
    :returns: TODO
    """
    print('parse_inner_brace: "{0}"'.format(function_string))
    inner_fun_regx = re.compile(
        r'(((\b[a-zA-Z]\w+\b)\.)?((\b[a-zA-Z]\w+\b)\s*\(([^()]*)\)))',
        re.IGNORECASE)

    while inner_fun_regx.search(function_string):
        m = inner_fun_regx.search(function_string)
        begin = m.start(1)
        end = m.end(1)
        function_result = process_inner(
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

ASSIGNMENT_OPERATORS = ['=']

COMPARISON_OPERATORS = ['=', '<>', '<', '>', '<=', '>=', ' is ']

CONCATENATION_OPERATORS = ['\&', '\+']

LOGICAL_OPERATORS = [' xor ', ' or ', ' and ', ' imp ', ' eqv ', ' not ']

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
