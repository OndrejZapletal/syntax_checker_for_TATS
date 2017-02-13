# Author: Ondrej Zapletal
# Date: 2016-02-01
# Description:
from prepare_for_checker import *


def test1():
    assert analyze_and_evaluate_reference_side(test_string1, 0, 0) == VALUE


def test2():
    assert analyze_and_evaluate_reference_side(test_string2, 0, 0) == VALUE


def test5():
    assert analyze_and_evaluate_reference_side(test_string5, 0, 0) == MISS_CLS


def test6():
    assert analyze_and_evaluate_reference_side(test_string13, 0, 0) == VALUE


def test7():
    assert analyze_and_evaluate_reference_side(test_string14, 0, 0) == VALUE


def test8():
    assert analyze_and_evaluate_reference_side(test_string15, 0, 0) == VALUE


def test9():
    assert analyze_and_evaluate_reference_side(
        function_with_1_invalid_paramter, 0, 0) == INVALID


def test_eval_sign_operator():
    assert evaluate_expression(
        sign_operator_with_different_number_of_whitespaces) == VALUE


def test_eval_string_operator():
    assert evaluate_expression(
        string_operator_with_different_number_of_whitespaces) == VALUE


def test_eval_wrong_whitespaces_resulting_in_missing_operator():
    assert evaluate_expression(
        string_operator_with_wrong_number_of_whitespaces) == MISSING_OPERATOR


def test_eval3():
    assert evaluate_expression(test_string7) == NULL


def test_eval4():
    assert evaluate_expression(test_string8) == NULL


def test_eval5():
    assert evaluate_expression(test_string9) == NULL


def test_eval6():
    assert evaluate_expression(test_string10) == NULL


def test_eval7():
    assert evaluate_expression(test_string10) == NULL


def test_eval8():
    assert evaluate_expression(test_string11) == NULL


def test_eval9():
    assert evaluate_expression(test_string12) == MISSING_OPERATOR


def test_eval10():
    assert evaluate_expression(
        operands_separated_by_operator_with_null) == NULL


def test_eval11():
    assert evaluate_expression(test_string16) == VALUE


test_string1 = "var + dVDR.Function(l1_a1, l1_a2)"
test_string2 = "fun1(arg1, dVDR.fun2(fun3()), arg4)"
test_string5 = "fun1(fun2(arg1 And arg2,fun3(),arg3,fun4(arg1,fun5()))))"

sign_operator_with_different_number_of_whitespaces = \
    " #VALUE#+  #VALUE# * #VALUE# &#VALUE#/#VALUE#"
string_operator_with_different_number_of_whitespaces = \
    "#VALUE#  or #VALUE# not #VALUE# AND   #VALUE# "
string_operator_with_wrong_number_of_whitespaces = \
    " #VALUE#  or #VALUE#not #VALUE# AND   #VALUE#"
test_string7 = " #VALUE#+#VALUE# * #VALUE#+#VALUE# and #NULL# "
test_string8 = "#VALUE# + #NULL# Or #VALUE#"
test_string9 = "#VALUE#\ #VALUE# + #VALUE# / #NULL#"
test_string10 = "#NULL#\ #NULL# + #NULL# / #NULL#"
test_string11 = "#NULL# #NULL# + #NULL# / #NULL#"
test_string11 = "#NULL# * #NULL# + #NULL# / #NULL#"
test_string12 = \
    "#VALUE#*#VALUE#\#VALUE##VALUE#+#NULL# &  #VALUE#^#VALUE# mod #VALUE#"
test_string13 = "fun1(arg1 + arg2 + argr + func3())"
test_string14 = "fun1(fun2(arg1 And arg2, fun3() + arg3, fun4(arg1, fun5())))"
test_string15 = \
    'OutputLog (1, STR_MSG_FAIL & " ******* SDU state is NOCOMM *******")'
test_string16 = \
    '( (InStr(Result,"LINE 2 OF MESSAGE") > 0 )  And ( (InStr(Result,"LINE 7 OF MESSAGE") > 0 ) ) And ( (InStr(Result,"MESSAGE INCOMPLETE") > 0 ) ) )'
function_with_1_invalid_paramter = \
    "Array( &H0,    &H1189, &H2312, &H329B, &H4624, &H57AD, &H6536, &H74BF, \
    &H8C48, &H9DC1, &HAF5A, &HBED3, &HCA6C, &HDBE5, &HE97E, &HF8F7, &H1081, \
    &H108,  &H3393, &H221A, &H56A5, &H472C, &H75B7, &H643E, &H9CC9, &H8D40, \
    &HBFDB, &HAE52, &HDAED, &HCB64, &HF9FF, &HE876, &H2102, &H308B, &H210,  \
    &H1399, &H6726, &H76AF, &H4434, &H55BD, &HAD4A, &HBCC3, &H8E58, &H9FD1, \
    &HEB6E, &HFAE7, &HC87C, &HD9F5, &H3183, &H200A, &H1291, &H318,  &H77A7, \
    &H662E, &H54B5, &H453C, &HBDCB, &HAC42, &H9ED9, &H8F50, &HFBEF, &HEA66, \
    &HD8FD, &HC974, &H4204, &H538D, &H6116, &H709F, &H420,  &H15A9, &H2732, \
    &H36BB, &HCE4C, &HDFC5, &HED5E, &HFCD7, &H8868, &H99E1, &HAB7A, &HBAF3, \
    &H5285, &H430C, &H7197, &H601E, &H14A1, &H528,  &H37B3, &H263A, &HDECD, \
    &HCF44, &HFDDF, &HEC56, #NULL#, &H8960, &HBBFB, &HAA72, &H6306, &H728F, \
    &H4014, &H519D, &H2522, &H34AB, &H630,  &H17B9, &HEF4E, &HFEC7, &HCC5C, \
    &HDDD5, &HA96A, &HB8E3, &H8A78, &H9BF1, &H7387, &H620E, &H5095, &H411C, \
    &H35A3, &H242A, &H16B1, &H738,  &HFFCF, &HEE46, &HDCDD, &HCD54, &HB9EB, \
    &HA862, &H9AF9, &H8B70, &H8408, &H9581, &HA71A, &HB693, &HC22C, &HD3A5, \
    &HE13E, &HF0B7, &H840,  &H19C9, &H2B52, &H3ADB, &H4E64, &H5FED, &H6D76, \
    &H7CFF, &H9489, &H8500, &HB79B, &HA612, &HD2AD, &HC324, &HF1BF, &HE036, \
    &H18C1, &H948,  &H3BD3, &H2A5A, &H5EE5, &H4F6C, &H7DF7, &H6C7E, &HA50A, \
    &HB483, &H8618, &H9791, &HE32E, &HF2A7, &HC03C, &HD1B5, &H2942, &H38CB, \
    &HA50,  &H1BD9, &H6F66, &H7EEF, &H4C74, &H5DFD, &HB58B, &HA402, &H9699, \
    &H8710, &HF3AF, &HE226, &HD0BD, &HC134, &H39C3, &H284A, &H1AD1, &HB58,  \
    &H7FE7, &H6E6E, &H5CF5, &H4D7C, &HC60C, &HD785, &HE51E, &HF497, &H8028, \
    &H91A1, &HA33A, &HB2B3, &H4A44, &H5BCD, &H6956, &H78DF, &HC60,  &H1DE9, \
    &H2F72, &H3EFB, &HD68D, &HC704, &HF59F, &HE416, &H90A9, &H8120, &HB3BB, \
    &HA232, &H5AC5, &H4B4C, &H79D7, &H685E, &H1CE1, &HD68,  &H3FF3, &H2E7A, \
    &HE70E, &HF687, &HC41C, &HD595, &HA12A, &HB0A3, &H8238, &H93B1, &H6B46, \
    &H7ACF, &H4854, &H59DD, &H2D62, &H3CEB, &HE70,  &H1FF9, &HF78F, &HE606, \
    &HD49D, &HC514, &HB1AB, &HA022, &H92B9, &H8330, &H7BC7, &H6A4E, &H58D5, \
    &H495C, &H3DE3, &H2C6A, &H1EF1, &HF78)"

operands_separated_by_operator_with_null = \
    "&H0    + &H1189 + &H2312 + &H329B + &H4624 + &H57AD + &H6536 + &H74BF +" \
    "&H8C48 + &H9DC1 + &HAF5A + &HBED3 + &HCA6C + &HDBE5 + &HE97E + &HF8F7 +" \
    "&H1081 + &H108  + &H3393 + &H221A + &H56A5 + &H472C + &H75B7 + &H643E +" \
    "&H9CC9 + &H8D40 + &HBFDB + &HAE52 + &HDAED + &HCB64 + &HF9FF + &HE876 +" \
    "&H2102 + &H308B + &H210  + &H1399 + &H6726 + &H76AF + &H4434 + &H55BD +" \
    "&HAD4A + &HBCC3 + &H8E58 + &H9FD1 + &HEB6E + &HFAE7 + &HC87C + &HD9F5 +" \
    "&H3183 + &H200A + &H1291 + &H318  + &H77A7 + &H662E + &H54B5 + &H453C +" \
    "&HBDCB + &HAC42 + &H9ED9 + &H8F50 + &HFBEF + &HEA66 + &HD8FD + &HC974 +" \
    "&H4204 + &H538D + &H6116 + &H709F + &H420  + &H15A9 + &H2732 + &H36BB +" \
    "&HCE4C + &HDFC5 + &HED5E + &HFCD7 + &H8868 + &H99E1 + &HAB7A + &HBAF3 +" \
    "&H5285 + &H430C + &H7197 + &H601E + &H14A1 + &H528  + &H37B3 + &H263A +" \
    "&HDECD + &HCF44 + &HFDDF + &HEC56 + #NULL# + &H8960 + &HBBFB + &HAA72 +" \
    "&H6306 + &H728F + &H4014 + &H519D + &H2522 + &H34AB + &H630  + &H17B9 +" \
    "&HEF4E + &HFEC7 + &HCC5C + &HDDD5 + &HA96A + &HB8E3 + &H8A78 + &H9BF1 +" \
    "&H7387 + &H620E + &H5095 + &H411C + &H35A3 + &H242A + &H16B1 + &H738  +" \
    "&HFFCF + &HEE46 + &HDCDD + &HCD54 + &HB9EB + &HA862 + &H9AF9 + &H8B70 +" \
    "&H8408 + &H9581 + &HA71A + &HB693 + &HC22C + &HD3A5 + &HE13E + &HF0B7 +" \
    "&H840  + &H19C9 + &H2B52 + &H3ADB + &H4E64 + &H5FED + &H6D76 + &H7CFF +" \
    "&H9489 + &H8500 + &HB79B + &HA612 + &HD2AD + &HC324 + &HF1BF + &HE036 +" \
    "&H18C1 + &H948  + &H3BD3 + &H2A5A + &H5EE5 + &H4F6C + &H7DF7 + &H6C7E +" \
    "&HA50A + &HB483 + &H8618 + &H9791 + &HE32E + &HF2A7 + &HC03C + &HD1B5 +" \
    "&H2942 + &H38CB + &HA50  + &H1BD9 + &H6F66 + &H7EEF + &H4C74 + &H5DFD +" \
    "&HB58B + &HA402 + &H9699 + &H8710 + &HF3AF + &HE226 + &HD0BD + &HC134 +" \
    "&H39C3 + &H284A + &H1AD1 + &HB58  + &H7FE7 + &H6E6E + &H5CF5 + &H4D7C +" \
    "&HC60C + &HD785 + &HE51E + &HF497 + &H8028 + &H91A1 + &HA33A + &HB2B3 +" \
    "&H4A44 + &H5BCD + &H6956 + &H78DF + &HC60  + &H1DE9 + &H2F72 + &H3EFB +" \
    "&HD68D + &HC704 + &HF59F + &HE416 + &H90A9 + &H8120 + &HB3BB + &HA232 +" \
    "&H5AC5 + &H4B4C + &H79D7 + &H685E + &H1CE1 + &HD68  + &H3FF3 + &H2E7A +" \
    "&HE70E + &HF687 + &HC41C + &HD595 + &HA12A + &HB0A3 + &H8238 + &H93B1 +" \
    "&H6B46 + &H7ACF + &H4854 + &H59DD + &H2D62 + &H3CEB + &HE70  + &H1FF9 +" \
    "&HF78F + &HE606 + &HD49D + &HC514 + &HB1AB + &HA022 + &H92B9 + &H8330 +" \
    "&H7BC7 + &H6A4E + &H58D5 + &H495C + &H3DE3 + &H2C6A + &H1EF1 + &HF78"
