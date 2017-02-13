# Author: Ondrej Zapletal                                                     #
# Date: 2015-12-17                                                            #
# Description: Second attempt to write class for TATS checker.                #
# KZN-2824: Create Syntax checker for TATS scripts                            #
#                                                                             #
# Currently used TATS IDE doesn't support  any source code analysis which can #
# sometime result in unobserved bugs which are very hard to find. For example #
# some identifier  is misspelled and  by the nature  of Visual Basic  that is #
# dynamically typed it  is very hard to find this  problem. The other problem #
# of  TATS IDE  is  that is  not  very good  tool and  it  doesn't have  many #
# features. This reflects in the way that many people that write TATS scripts #
# are  using some  other text  editors and  only use  TATS IDE  to run  these #
# scripts to find any potential problems. This is very ineffective and slow.  #
#                                                                             #
# I'm proposing  to create  syntax checker  for TATS in  python, that  can be #
# combined with several advanced text editors and crate alternative for TATS  #
# IDE.                                                                        #
#                                                                             #
# Syntax should be able to check following problems:                          #
# TODO                                                                        #
# - use of unassigned variables                                               #
# - function call that is not matching function prototype                     #
# - closing statement for all conditional and loop statements                 #
# - appliance with coding standard (this is not vital but it can be useful)   #
# - any statements that are not valid                                         #
# - detection of '_' (line break) that is followed by comment                 #
# Done                                                                        #
# - undeclared variables                                                      #
# - unused variables                                                          #
###############################################################################
# plan for features                                                           #
###############################################################################
# call of function or sub:                                                    #
# ^\s*call\s+(\w+)\s*\((.*)\)                                                 #
# group(1) = function name                                                    #
# group(2) = function parameters                                              #
#                                                                             #
# possible parameters of function:                                            #
# string              => const                                                #
# number              => const                                                #
# variable    => variable                                                     #
# function call  => function call                                             #
#                                                                             #
# Dim name                                                                    #
# Const name = value                                                          #
# check declaration format                                                    #
# check that Const is never used as l-value                                   #
# Private variableName                                                        #
# Class name                                                                  #
#                                                                             #
# Call functionName                                                           #
#                                                                             #
###############################################################################

# import glob
import os
# import re
import sys

# import cProfile
# import ipdb

from Constants import HELP_STRING, NAME, VERSION, AUTHOR, DATE
from TATS_Source import TatsSyntaxChecker


def process_arguments():
    # test for flags
    if len(sys.argv) < 2:
        print(
            "Error, there were no parameters passed."
            " For more information call with '-h' flag.")
    elif len(sys.argv) == 2:
        if sys.argv[1] == '--version' or sys.argv[1] == '-v':
            print(
                "{0} - {1}\nCreated By: {2}\nDate: {3}".format(
                    NAME, VERSION, AUTHOR, DATE))

        elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print(HELP_STRING)
        else:
            if os.path.isfile(sys.argv[1]):
                return True
            else:
                print(
                    "Error, '{0}' is not a valid file or flag. For more "
                    "information try call with '--help' or '-h' flag.".
                    format(sys.argv[1]))
                return False
    elif len(sys.argv) == 3:
        if os.path.isfile(sys.argv[1]) and \
                (int(sys.argv[2]) == 0 or int(sys.argv[2]) == 1 or
                    int(sys.argv[2]) == 2):
            return True
            # for k1, project in checker._projects.items():
            #     for k2 in sorted(
            # project._methods.keys(), key=lambda k2 : k2):
            #         print(project._methods[k2])
            #     for k2, cls in sorted(
            # project._classes.items(), key=lambda (k2, cls) : cls._name):
            #         print(cls._name)
            #         for k3, method    in sorted(
            #  cls._class_methods.items(),
            # key=lambda (k3, method) : method._name):
            #             print(method._name)
            #         print("")
            #     print(30*"*")
            #     for k2, functions in sorted(
            # project._functions.items(), key=lambda (k2, functions) :
            # functions._name):
            #         print(functions._name)
        else:
            print(
                "Error, '{0}' is not a valid file and/or third parameter "
                "is not 1 or 0. For more information try call with '--help'"
                " or '-h' flag.".format(sys.argv[1]))
            return False
    else:
        print(
            "Error, too many parameters passed. "
            "For more information call with '-h' flag.")
        return False

if process_arguments():
    checker = TatsSyntaxChecker(sys.argv[1])
    checker.parse_project_files()
    if len(sys.argv) > 2:
        checker.show_results(sys.argv[2])
    else:
        checker.show_results()
