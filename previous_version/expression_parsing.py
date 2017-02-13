# Author: Ondrej Zapletal
# Date: 2016-02-16
# Description:
import re
import ipdb
import logging


logging.basicConfig(filename='example.log', level=logging.DEBUG)
logging.info("Start:")


def find_functions(source_string):
    """find"""
    print("find_functions: {0}".format(source_string))
    logging.info("find_functions: {0}".format(source_string))
    regex_string = '((({0})|((\w+\.)?(\w+)))?\s*(\([^()]*\)))'.format(
            EVALUATING_OPERATORS)
    logging.info("find_functions:regex_string: {0}".format(regex_string))
    regex = re.compile(regex_string, re.IGNORECASE)
    if regex.search(source_string):
        m = regex.search(source_string)
        if m.group(3):  # expression in parentheses prefixed by operator
            return_value = \
                m.group(3) + " " + analyze_parents(m.group(7))
        elif m.group(5):  # method call
            return_value = analyze_method_call(m.group(1))
        elif m.group(6):  # function call
            if m.group(6).strip() in EXISTING_FUNCTIONS:
                return_value = analyze_function_call(m.group(1))
            else:
                return_value = "#UNKNOWN_IDEN#"
        elif m.group(7):  # plain expression in parentheses
            return_value = analyze_parents(m.group(1))
        else:
            # this might also meen that there is missing operator
            return_value = "error"
        return find_functions(
            source_string[:m.start(1)] + return_value +
            source_string[m.end(1):])
    else:
        return evaluate_plain_expression(source_string)


def analyze_method_call(string):
    logging.debug("analyze_method_call: {0}".format(string))
    return "#VALUE#"


def analyze_function_call(string):
    logging.debug("analyze_function_call: {0}".format(string))
    return "#VALUE#"


def analyze_parents(string):
    r_inside_brace = re.compile("\((.*)\)", re.IGNORECASE)
    m = r_inside_brace.search(string)
    logging.debug("analyze_parents: {0}".format(string))
    return evaluate_plain_expression(m.group(1))


def evaluate_plain_expression(source_string):
    """Function evaluates expression that is present in input source_string.

    @param source_string - contains expression
    @return: evaluated result of expression
        - #VALUE# - proper value
        - #NULL# - no return value (for example procedure call without return
        value instead of function call)
        - #MISSING_OPERATOR# - two values (identifiers of functions) are not
        correctly separated by operand (either operand is missing entirely or
        it has improper format)
        - #MISSING_CLOSING#/#MISSING_OPENING# - expression has unpared brace
        - #INVALID# - TODO: certin part of expression is invalid.
    """
    logging.info('evaluate_plain_expression: "{0}"'.format(source_string))
    evaluation_string = \
        r'\s*({0}|{1}|{2})\s*({3})\s*({0}|{1}|{2})(.*)'.format(
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
    if source_string == "":
        return ""
    elif re.search('[(]', source_string):
        return MISS_CLS
    elif re.search('[)]', source_string):
        return MISS_OPN
    elif single_value_regex.match(source_string):
        single_value_match = single_value_regex.match(source_string)
        return analyze_identifier_reference(single_value_match.group(1))
    elif evaluation_regex.match(source_string):
        evaluation_match = evaluation_regex.match(source_string)
        arg1 = analyze_identifier_reference(evaluation_match.group(1))
        if evaluation_match.group(4):
            operator = analyze_identifier_reference(evaluation_match.group(4))
        else:
            operator = ""
        arg2 = analyze_identifier_reference(evaluation_match.group(5))
        source_string = return_value_of_expression(arg1, operator, arg2)

        if evaluation_match.group(8):
            return evaluate_plain_expression(
                source_string + evaluation_match.group(8))
        else:
            return source_string
    elif contains_invalid_regex.match(source_string):
        return INVALID
    elif missing_operator_regex.match(source_string):
        return MISS_OPR
    else:
        ipdb.set_trace()  # #BREAKPOINT#


def return_value_of_expression(arg1, oper, arg2):
    """Function takes two operands and operator to compute result of expression
    @param arg1 - operand left
    @param oper - operator
    @param arg2 - operand right
    @return: result of operator operation
    """
    logging.debug('return_value_of_expression: "{0}", "{1}", "{2}"'.format(
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


def analyze_identifier_reference(word):
    """Function estimates all necessary states about identifier and triggers
    Error or Warnings.

    @param word: identifier or operator
    @return: TODO: value of identifier

    """
    logging.debug('analyze_identifier_reference: "{0}"'.format(word))
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


EXISTING_FUNCTIONS = ['InStr', 'fun2', 'fun3']
OPERATORS = ["\+", "-", "\*", "/", "and", "or"]
OP = '|'.join(OPERATORS)

ARITHMETIC_OPERATORS = ['\*', '\/', '\+', '-', ' mod ', '\&', r'\\', '\^']
ARITHMETIC_OPERATORS_NOSPACE = \
        ['\*', '\/', '\+', '-', 'mod', '\&', r'\\', '\^']

ASSIGNMENT_OPERATORS = ['=']

COMPARISON_OPERATORS = ['=', '<>', '<', '>', '<=', '>=', ' is ']
COMPARISON_OPERATORS_NOSPACE = ['=', '<>', '\<', '\>', '<=', '>=', 'is']

CONCATENATION_OPERATORS = ['\&', '\+']

LOGICAL_OPERATORS = [' xor ', ' or ', ' and ', ' imp ', ' eqv ', ' not ']
LOGICAL_OPERATORS_NOSPACE = ['xor', 'or', 'and', 'imp', 'eqv', 'not']

IDENTIFIER = '(".*?"|&\w+|\w+|[+-]?\d+(\.\d+)?)'

ALL_OPERATORS = ARITHMETIC_OPERATORS_NOSPACE + ASSIGNMENT_OPERATORS + \
    COMPARISON_OPERATORS_NOSPACE + CONCATENATION_OPERATORS + \
    LOGICAL_OPERATORS_NOSPACE

MISS_CLS = "#MISSING_CLOSING#"
MISS_OPN = "#MISSING_OPENING#"
MISS_OPR = "#MISSING_OPERATOR#"
VALUE = "#VALUE#"
NULL = "#NULL#"
OPERATOR = "#OPERATOR#"
INVALID = "#INVALID#"
IDENTIFIER = '(".*?"|&\w+|\w+|[+-]?\d+(\.\d+)?)'

EVALUATING_OPERATORS = "{0}".format('|'.join(ALL_OPERATORS))

source = 'variable = (oj.fun1(variable +(' \
    'value *fun3(val)and fun3(variable2))) * fun2()) and 1'

source2 = '(InStr(Result,"LINE 2 OF MESSAGE")>0)And((InStr(' \
    'Result,"LINE 7 OF MESSAGE")>0))And((InStr(Result,' \
    '"MESSAGE INCOMPLETE")>0))'

logging.debug("find_functions: {0}".format(
    find_functions(source2)))
