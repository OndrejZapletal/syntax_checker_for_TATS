# -*- coding: utf-8 -*-
# Author: Ondrej Zapletal
# Date: 2016-03-09
# Description:

import glob
import os
import re
import sys
import ipdb

from lexer import statements_extractions

from Constants import ALL_KEYWORDS, VALUE, NULL, OPERATOR, INVALID, \
    MISS_OPE, MISS_CLS, MISS_OPN, IDENTIFIER, ALL_OPERATORS, \
    EVALUATING_OPERATORS

from TATS_Classes import IdentifierRepresentation, FunctionRepresentation, \
    MethodRepresentation, ClassRepresentation, DefectRepsentation

for file_name in glob.glob('*.tsf'):
    with open(file_name, 'r') as source:
        statements = source.read()
        print(file_name)
        for lexical_statement in statements_extractions(statements):

            print("\t", lexical_statement)
            print()


class TatsSyntaxChecker(object):
    """Class is keeping information about all projects that contain specified
    TATS file.
    """

    def __init__(self, origination_file):
        """Object is initialized with file name that is checked. This file is
        used through out this project as a reference to the file of interest.
        For example by default only errors that originate in this file are
        listed.

        :origination_file: file that orignates syntax check
        """
        self._origination_file = os.path.abspath(origination_file)
        self._errors = list()
        self._project_files = list()
        self._projects = dict()

    def parse_project_files(self):
        """ Finds project files that contain examined script file. This
        complicates things a little since some files can be found in multiple
        different projects. It calls function analyze_project for each found
        project or for stand alone file.
        """
        self._project_files = self.find_project_source()
        if len(self._project_files) != 0:
            for project_file in self._project_files:
                self._projects[project_file] = TatsProject(
                    self._origination_file)
                self._projects[project_file].analyze_project(project_file)
                self._errors = self._errors + \
                    self._projects[project_file]._errors
        else:
            self._projects[self._origination_file] = TatsProject(
                self._origination_file)
            self._projects[self._origination_file].analyze_project()
            self._errors = self._errors + \
                self._projects[self._origination_file]._errors

    def find_project_source(self):
        """ Creates and returns list of project files that contain examined
        source file within them.

        :returns: list of projects containing examined source file
        """
        project_sources = list()
        if self.search_in_curr_directory(project_sources):
            return project_sources
        elif self.search_in_env_directory(project_sources):
            return project_sources
        else:
            return list()

    def search_in_curr_directory(self, project_sources):
        """ Find all *.tsp files in current directory and extract the ones that
        contain self._origination_file

        :project_sources: List of project source files that is used as result
        in method parse_project_files
        :returns: True if any project files were found, False if not.
        """
        tsf_file = re.compile('"(.*\.tsf)"')
        project_files_found = False
        files_in_direct = glob.glob('*.tsp')
        for file_name in files_in_direct:
            with open(file_name, 'r') as file:
                for line in file:
                    if tsf_file.search(line):
                        if os.path.abspath(tsf_file.search(line).group(1)) == \
                                self._origination_file:
                            project_sources.append(file_name)
                            project_files_found = True
                            break
        return project_files_found

    def search_in_env_directory(self, project_sources):
        """ Searches for *.tsp files in Test_Env directory for
        self._origination_file

        :project_sources: empty parameter that is poulated by list of found
        project files containing examined file
        :returns: True if file is contained within examined file False
        otherwise
        """
        tsf_file = re.compile('"(.*\.tsf)"')
        project_files_found = False
        files_in_direct = glob.glob('..\Test_Env\*.tsp')
        for file_name in files_in_direct:
            with open(file_name, 'r') as file:
                for line in file:
                    if tsf_file.search(line):
                        if tsf_file.search(line).group(1) == \
                                self._origination_file:
                            project_sources.append(file_name)
                            project_files_found = True
                            break
        return project_files_found

    def show_results(self, debug=0):
        """Method prints all defects based on user settings

        @param debug:
            0 - defaultly only defects introduced in origination_file are
            outputed
            1 - all errors are outputed
            2 - some errors are shown as warnings. Not finished TODO
        @return: None
        """
        if int(debug) == 1:
            for error in sorted(sorted(self._errors,
                                key=lambda x: x._line_number),
                                key=lambda x: x._source_file):
                print('{0}:{1}:{2}: {3}'.format(
                        error._source_file, error._line_number, 0,
                        error._error_description))
        elif int(debug) == 2:
            for error in sorted(sorted(self._errors,
                                key=lambda x: x._line_number),
                                key=lambda x: x._source_file):
                if error._source_file == self._origination_file:
                    if "Undeclared" in error._error_description:
                        print('{0}:{1}:{2}: {3}'.format(
                                os.path.basename(error._source_file),
                                error._line_number, 0,
                                "WARNING: " + error._error_description))
                    else:
                        print('{0}:{1}:{2}: {3}'.format(
                                os.path.basename(error._source_file),
                                error._line_number, 0,
                                "ERROR: " + error._error_description))
        else:
            for error in sorted(sorted(self._errors,
                                key=lambda x: x._line_number),
                                key=lambda x: x._source_file):
                if error._source_file == self._origination_file:
                    print('{0}:{1}:{2}: {3}' % (
                        error._source_file, error._line_number, 0,
                        error._error_description))


class TatsProject(object):
    """Class that will contain TATS project information."""

    def __init__(self, origination_file):
        """Class has to be initiated with name of calling file for which we
        will do the analysis.

        @param origination_file - name of file that the syntax checker is
        called for
        @return: TODO

        """
        # TODO
        self._tats_project_file_path = ""

        # declared identifiers - list of identifiers that have been declared in
        # global name space.
        self._declared_identifiers = dict()

        # unassigned identifiers - list of identifiers that have been declared
        # in global name space but never assigned any value
        self._unassigned_identifiers = dict()

        # unassigned used identifiers - list of identifiers that have been
        # declared in global name space, never assigned any value, but used.
        self._unassigned_used_identifiers = dict()

        # unused identifiers - list of identifiers that have been declared and
        # assigned in global name space but never used.
        self._unused_identifiers = dict()

        # undeclared identifiers - list of identifiers that haven't been
        # declared in global name space. This means that they are not declared
        # as variable nor constant nor as a function.
        self._undeclared_identifiers = dict()

        # list of functions that are found in project
        self._functions = dict()

        # list of classes that are found in project
        self._classes = dict()

        # list of methods that are found in project
        self._methods = dict()

        # contains information whether is file option explicit
        self._file_option_explicit = dict()

        # TODO
        self._errors = list()

        # file that triggered analysis
        self._origination_file = origination_file

    def identifier_referencing_global(self, name, line_number, file_name):
        name = name.strip()
        l_name = name.lower()

        if l_name not in ALL_KEYWORDS and \
                l_name != '':
            if l_name not in  \
                    self._declared_identifiers.keys() and \
                    l_name not in \
                    self._undeclared_identifiers.keys() and \
                    l_name not in self._functions.keys():

                # new undeclared identifier
                self._undeclared_identifiers[l_name] = \
                        IdentifierRepresentation(
                                name, line_number,
                                file_name,
                                "identifier")
                if self._file_option_explicit[file_name]:
                    self._errors.append(DefectRepsentation(
                            name, "Undeclared identifier",
                            file_name,
                            line_number))
            elif l_name in self._declared_identifiers.keys():
                try:
                    del self._unused_identifiers[l_name]
                except KeyError:
                    pass
            elif l_name in self._functions.keys():
                self._functions[l_name]._called = True
                self.analyze_funtion(l_name)

    def lex_and_parse(self, file_lines):
        """TODO: Docstring for lex_and_parse.

        @param file_lines TODO
        @return: TODO

        """
        pass

    def analyze_project(self, project_file=''):
        """Parses TATS project file and each found TATS script file is further
        decomposed.
        STEPS:
            1. Names of individual script files are parsed from project source
            file. In case that no project source file is provided,
            origination_file is analyzed as standalone.
            2. Each script file is opened and split into list of lines.
            3. prepare_file function is called to remove line brakes for
            simpler analysis
            4. parse_classes function is called to separate global name space
            from class name space. Only lines of class are removed and header
            is analyzed. Analysis of class itself is postponed until first
            object is created.
            5. parse_functions is called to to separate function definitions
            from global name space.
            6. parse_variables is called to analyze global name space.
            7. All unused identifiers and functions are listed as potential
            warnings

        :project_file: path of source of TATS project
        :returns: TODO - so far no return
        """
        file_string = ""
        if project_file != '':
            tsf_file = re.compile('"(.*\.tsf)"')
            scripts_in_project = list()
            with open(project_file, 'r') as file:
                for line in file:
                    if tsf_file.search(line):
                        file_string = os.path.abspath(
                                tsf_file.search(line).group(1).lower())
                        scripts_in_project.append(file_string)
                        self._file_option_explicit[file_string] = False
        else:
            scripts_in_project = [self._origination_file]
            self._file_option_explicit[self._origination_file] = False

        # this is where the actual parsing of namespaces is done
        for file_name in scripts_in_project:
            with open(file_name, 'r') as file:
                file_content = file.read().split("\n")
                lex_and_parse(file_content)

            # after all files are analzed all identifier left unreferenced are
            # noted
            for k, v in self._functions.items():
                if not v._called:
                    self._errors.append(DefectRepsentation(
                        v._name, "Unused function", v._declaration_source_file,
                        v._declaration_line_number))

            for k, v in self._unused_identifiers.items():
                self._errors.append(DefectRepsentation(
                    v._name, "Unused " + v._identifier_type,
                    v._declaration_source_file, v._declaration_line_number))

    def prepare_file(self, file_name):
        """ Replaces all lines that are broken down by _ character into single
        long line. Original lines that were bellow first line are replaced by
        empty line, to preserve an information about line number in original
        file. Also information about Option Explicit is extracted from each
        file.

        :file_name: of file that will be prepared
        :returns: contetn of file in list of lines seperatd by newline
        character
        """
        # identification of lines with option explicit regex
        opt_explicit = re.compile('^\s*option\s+explicit', re.IGNORECASE)
        remove_linebreak = re.compile(r'_\s*$', re.IGNORECASE)
        with open(file_name, 'r') as file:
            file_content_lines = file.read().split("\n")

        broken_line = False
        broken_line_index = 0
        file_content_lines_temp = file_content_lines[:]

        for i, line in enumerate(file_content_lines):
            if opt_explicit.match(line):
                self._file_option_explicit[file_name] = True
            if not broken_line:
                if remove_linebreak.search(line):
                    broken_line = True
                    broken_line_index = i
                    break_character_index = line.rfind('_')
                    file_content_lines_temp[i] = line[:break_character_index]
            else:
                if remove_linebreak.search(line):
                    break_character_index = line.rfind('_')
                    file_content_lines_temp[broken_line_index] = \
                        file_content_lines_temp[broken_line_index] + ' ' + \
                        line[:break_character_index]
                    file_content_lines_temp[i] = ""
                else:
                    file_content_lines_temp[broken_line_index] = \
                        file_content_lines_temp[broken_line_index] + ' ' + \
                        line
                    file_content_lines_temp[i] = ""
                    broken_line = False
        return file_content_lines_temp

    # def parse_name_space(
    #   self, file_content_lines, file_name, line_offset, name_space=GLOBAL):
    def parse_variables(self, file_content_lines, file_name, line_offset):
        """TODO: Docstring for parse_variables.

        :file_content_lines: TODO
        :file_name: TODO
        :returns: TODO
        """
        # strings regex
        substitute_string = re.compile('".+"', re.IGNORECASE)
        # hexadecimal constants regex
        remove_hexa = re.compile(r'&\b\w+\b', re.IGNORECASE)
        # integer constants regex
        remove_integer = re.compile(r'\b\d+\b', re.IGNORECASE)
        # comments regex
        remove_comments = re.compile("'.*$", re.IGNORECASE)

        # identification of lines with declaration regex
        declaration = re.compile(
                r"^\s*(\bpublic\b|\bprivate\b|\bconst\b|\bdim\b|\bredim\b)",
                re.IGNORECASE)
        method_call = re.compile(r'\b[a-z]\w+\b\.\b[a-z]\w+\b', re.IGNORECASE)
        function_call = re.compile(
                r'\s*call\s+\b[a-z]\w+\b[^.]', re.IGNORECASE)
        # if_statement
        # for_loop
        # while_loop
        # select_case

        word_delimiter = re.compile("[^\w]", re.IGNORECASE)
        blank_line = re.compile('^\s*$')

        for i, line in enumerate(file_content_lines):
            line = remove_comments.sub('', line, sys.maxsize)
            line = substitute_string.sub('const', line, sys.maxsize)
            line = remove_hexa.sub('const', line, sys.maxsize)
            line = remove_integer.sub('const', line, sys.maxsize)
            if blank_line.match(line):
                pass
            elif declaration.match(line):
                self.parse_declaration(line, line_offset + i, file_name)
            # elif if_statement.match(line):

            elif method_call.match(line):
                self.parse_method_call(line, line_offset + i, file_name)
            elif function_call.match(line):
                self.parse_function_call(line, line_offset + i, file_name)
            else:
                for variables in word_delimiter.split(line):
                    self.identifier_referencing_global(
                            variables, line_offset + i, file_name)

    def parse_function_call(self, line, line_offset, file_name):
        """TODO: Docstring for parse_function_call.

        :line: TODO
        :line_offset: TODO
        :file_name: TODO
        :returns: TODO

        """
        function_call = re.compile(
                r'\s*call\s+(\b[a-z]\w+\b)[^.]\s*\((.*)\)?', re.IGNORECASE)
        array_parents = re.compile('\(.*?\)', re.IGNORECASE)
        parameters = ""
        identifier = list()
        try:
            function_name = function_call.match(line).group(1).lower()
        except AttributeError:
            ipdb.set_trace()  # #BREAKPOINT#
        try:
            parameters = function_call.match(line).group(2)
            parameters = array_parents.sub('()', parameters, sys.maxsize)
        except AttributeError:
            parameters = ""

        if function_name in self._functions.keys():
            self._functions[function_name]._called = True
            self.analyze_funtion(function_name)

        for identifier in parameters.split(','):
            identifier = identifier.strip()
            l_identifier = identifier.lower()
            if l_identifier not in ALL_KEYWORDS and \
                    l_identifier != '':
                if l_identifier not in self._declared_identifiers.keys() and \
                        l_identifier not in \
                        self._undeclared_identifiers.keys() and \
                        l_identifier not in self._functions.keys():
                    # new undeclared identifier
                    self._undeclared_identifiers[l_identifier] = \
                            IdentifierRepresentation(
                                    identifier, line_offset,
                                    file_name, 'identifier')
                    if self._file_option_explicit:
                        self._errors.append(DefectRepsentation(
                                identifier, 'Undeclared identifier',
                                file_name, line_offset))
                elif l_identifier in self._declared_identifiers.keys():
                    try:
                        del self._unused_identifiers[l_identifier]
                    except KeyError:
                        pass
                elif l_identifier in self._functions.keys():
                    self._functions[l_identifier]._called = True
                    self.analyze_funtion(l_identifier)

    def parse_method_call(self, line, line_offset, file_name):
        """TODO: Docstring for parse_method_call.

        :line: TODO
        :line_offset: TODO
        :file_name: TODO
        :returns: TODO
        """
        method_call = re.compile(
                r'\s*call\s+(\b\w+\b)\.(\b\w+\b)(\((.*)\))?', re.IGNORECASE)
        method_assign = re.compile(
                r'\s*(\b\w+\b)\s*\=\s*(\b\w+\b)\.(\b\w+\b)(\((.*)\))?',
                re.IGNORECASE)
        method_self = re.compile(
                r'\s*(\b\w+\b)\.(\b\w+\b)(\((.*)\))?', re.IGNORECASE)
        substitute_string = re.compile('".*"', re.IGNORECASE)
        remove_hexa = re.compile(r'&\b\w+\b', re.IGNORECASE)
        remove_integer = re.compile(r'\b\d+\b', re.IGNORECASE)
        array_parents = re.compile('\(.*?\)', re.IGNORECASE)

        line = substitute_string.sub('const', line, sys.maxsize)
        line = remove_hexa.sub('const', line, sys.maxsize)
        line = remove_integer.sub('const', line, sys.maxsize)

        assigment = ""
        object_name = ""
        method_name = ""
        method_paramters = ""
        identifiers = list()

        local_option_explicit = self._file_option_explicit[file_name]

        if method_call.match(line):
            # ipdb.set_trace() #BREAKPOINT#
            object_name = method_call.match(line).group(1)
            method_name = method_call.match(line).group(2)
            try:
                method_paramters = method_call.match(line).group(4)
            except AttributeError:
                method_paramters = ""
        elif method_assign.match(line):
            assigment = method_assign.match(line).group(1)
            object_name = method_assign.match(line).group(2)
            method_name = method_assign.match(line).group(3)
            try:
                method_paramters = method_assign.match(line).group(5)
            except AttributeError:
                method_paramters = ""
        elif method_self.match(line):
            object_name = method_self.match(line).group(1)
            method_name = method_self.match(line).group(2)
            try:
                method_paramters = method_self.match(line).group(4)
            except AttributeError:
                method_paramters = ""
        else:
            ipdb.set_trace()  # #BREAKPOINT#
            pass
        if assigment != "":
            identifiers.append(assigment)
        if method_paramters != "":
            try:
                method_paramters = array_parents.sub(
                        '()', method_paramters, sys.maxsize)
            except TypeError:
                method_paramters = ""
                # ipdb.set_trace() #BREAKPOINT#
                pass
            for identifier in method_paramters.split(','):
                identifiers.append(identifier)
        identifiers.append(object_name)
        if method_name.lower() not in self._methods.keys():
            self._errors.append(DefectRepsentation(
                    method_name, 'Undefined method',
                    file_name, line_offset))
        for identifier in identifiers:
            identifier = identifier.strip()
            l_identifier = identifier.lower()
            if l_identifier not in ALL_KEYWORDS and \
                    l_identifier != '':
                if l_identifier not in self._declared_identifiers.keys() and \
                        l_identifier not in \
                        self._undeclared_identifiers.keys() and \
                        l_identifier not in self._functions.keys():
                    # new undeclared identifier
                    self._undeclared_identifiers[l_identifier] = \
                            IdentifierRepresentation(
                                    identifier, line_offset,
                                    file_name, 'identifier')
                    if local_option_explicit:
                        self._errors.append(DefectRepsentation(
                                identifier, 'Undeclared identifier',
                                file_name, line_offset))
                elif l_identifier in self._declared_identifiers.keys():
                    try:
                        del self._unused_identifiers[l_identifier]
                    except KeyError:
                        pass
                elif l_identifier in self._functions.keys():
                    self._functions[l_identifier]._called = True
                    self.analyze_funtion(l_identifier)

    def parse_declaration(self, line, line_number, file_name, scope='glob'):
        """TODO: Docstring for parse_declaration.

        :line: TODO
        :line_number: TODO
        :file_name: TODO
        :scope: TODO
        :returns: TODO
        """
        identifier_name = ""
        array_parents = re.compile('\(.*?\)', re.IGNORECASE)
        dim_type = re.compile('^\s*dim\s+(.+)', re.IGNORECASE)
        const_type = re.compile(
                '^\s*((public|private)\s)?\s*const\s+(.*)', re.IGNORECASE)
        redim_type = re.compile(
                '^\s*redim\s+(preserve\s)?\s*(.*)', re.IGNORECASE)
        public_type = re.compile(
                '^\s*((public)\s)\s*(.*)', re.IGNORECASE)
        private_type = re.compile(
                '^\s*((private)\s)\s*(.*)', re.IGNORECASE)

        if const_type.match(line):
            identifier_name = re.match(
                    '^\s*((public|private)\s)?\s*const\s+(\w+)', line,
                    re.IGNORECASE).group(3)
            l_identifier_name = identifier_name.lower()
            if not re.match(
                    '^\s*((public|private)\s)?\s*const\s+(\w+)\s*=\s*" \
                    "([+-]?\d+|".+"|&\w+|)',
                    line, re.IGNORECASE):
                self._errors.append(DefectRepsentation(
                        identifier_name, 'Constant in incorrect format',
                        file_name, line_number))
            self._declared_identifiers[l_identifier_name] = \
                IdentifierRepresentation(
                    identifier_name, line_number, file_name,
                    'constant')
            self._unused_identifiers[l_identifier_name] = \
                IdentifierRepresentation(
                    identifier_name, line_number, file_name,
                    'constant')
        else:
            if dim_type.match(line):
                variables = dim_type.match(line).group(1)
            elif redim_type.match(line):
                variables = redim_type.match(line).group(2)
            elif private_type.match(line):
                variables = private_type.match(line).group(3)
            elif public_type.match(line):
                variables = public_type.match(line).group(3)
            else:
                ipdb.set_trace()  # #BREAKPOINT#

            variables = array_parents.sub('()', variables, sys.maxsize)

            for identifier_name in variables.split(','):
                try:
                    identifier_name = re.match(
                        '^\s*(\w+)(\(.*\))?\s*$', identifier_name).group(1)
                    l_identifier_name = identifier_name.lower()
                    self._declared_identifiers[l_identifier_name] = \
                        IdentifierRepresentation(
                                identifier_name, line_number,
                                file_name, 'variable')
                    self._unused_identifiers[l_identifier_name] = \
                        IdentifierRepresentation(
                            identifier_name, line_number,
                            file_name, 'variable')
                except AttributeError:
                    self._errors.append(
                        DefectRepsentation(
                            identifier_name,
                            'List of identifers is incorrectly seperated',
                            file_name, line_number))

    def parse_classes(self, file_content_lines, file_name):
        """TODO: Docstring for parse_classes.

        :arg1: TODO
        :returns: TODO
        """
        class_header = re.compile('\s*class\s+(\w+)', re.IGNORECASE)
        class_end = re.compile('\s*end\s+class', re.IGNORECASE)

        class_start_line = 0
        in_class = False
        global_file_content = list()
        class_lines = list()
        class_name = ""
        for i, line in enumerate(file_content_lines):
            if class_header.match(line):
                in_class = True
                class_start_line = i + 1
                try:
                    class_name = class_header.match(line).group(1)
                except AttributeError:
                    pass
                class_lines = list()
                class_lines.append(line)
                global_file_content.append("")
            elif class_end.match(line):
                in_class = False
                class_lines.append(line)
                global_file_content.append("")
                self._classes[class_name.lower()] = ClassRepresentation(
                        class_name, class_start_line,
                        file_name, class_lines)
                self.parse_methods(class_name)
                # self.analyze_class(class_name)
            elif in_class:
                class_lines.append(line)
                global_file_content.append("")
            else:
                global_file_content.append(line)
        return global_file_content

    def parse_methods(self, class_name):
        """TODO:

        :arg1: TODO
        :returns: TODO
        """
        header = re.compile(
                r'\s*((public|private)\s+)?(function|sub)\s+(\w+)',
                re.IGNORECASE)
        # header2 = re.compile(r'\s*(function|sub)\s+(\w+)', re.IGNORECASE)
        end = re.compile('\s*(end)\s+(function|sub)', re.IGNORECASE)
        sub = False
        private = False
        l_class_name = class_name.lower()

        try:
            file_content_lines = self._classes[l_class_name]._class_lines
        except KeyError:
            ipdb.set_trace()  # #BREAKPOINT#
        file_name = self._classes[l_class_name]._declaration_source_file

        method_start_line = 0
        in_method = False
        global_file_content = list()
        method_lines = list()
        method_name = ""

        for i, line in enumerate(file_content_lines):
            if header.match(line):
                in_method = True
                method_start_line = i + 1
                try:
                    if header.match(line).group(2).lower() == "private":
                        private = True
                except AttributeError:
                    private = False
                if header.match(line).group(3).lower() == "sub":
                    sub = True
                method_name = header.match(line).group(4)
                l_method_name = method_name.lower()
                method_lines = list()
                method_lines.append(line)
                global_file_content.append("")
            elif end.match(line):
                in_method = False
                method_lines.append(line)
                global_file_content.append("")
                self._classes[l_class_name]._class_methods[l_method_name] = \
                    MethodRepresentation(
                            method_name, method_start_line,
                            file_name, method_lines,
                            class_name, sub, private)
                if l_method_name not in self._methods.keys():
                    self._methods[l_method_name] = method_name
            elif in_method:
                method_lines.append(line)
                global_file_content.append("")
            else:
                global_file_content.append(line)
        return global_file_content

    def parse_functions(self, file_content_lines, file_name):
        """ TODO:

        :file_content_lines: TODO
        :file_name: TODO
        :returns: TODO
        """
        header = re.compile(
                '\s*((public|private)\s+)?(function|sub)\s+(\w+)',
                re.IGNORECASE)
        end = re.compile('\s*(end)\s+(function|sub)', re.IGNORECASE)
        sub = False
        private = False
        in_function = False
        function_start_line = 0
        global_file_content = list()
        function_lines = list()
        function_name = ""
        for i, line in enumerate(file_content_lines):
            if header.match(line):
                in_function = True
                function_start_line = i + 1
                try:
                    if header.match(line).group(2).lower() == "private":
                        private = True
                except AttributeError:
                    private = False
                if header.match(line).group(3).lower() == "sub":
                    sub = True
                function_name = header.match(line).group(4)
                l_function_name = function_name.lower()
                function_lines = list()
                function_lines.append(line)
                global_file_content.append("")
            elif end.match(line):
                in_function = False
                function_lines.append(line)
                global_file_content.append("")
                self._functions[l_function_name] = FunctionRepresentation(
                        function_name, function_start_line,
                        file_name, function_lines, sub,
                        private)
            elif in_function:
                function_lines.append(line)
                global_file_content.append("")
            else:
                global_file_content.append(line)
        return global_file_content

    def analyze_class(self, class_name):
        """TODO: Docstring for analyze_class.

        :class_name: TODO
        :returns: TODO

        """
        pass

    def analyze_funtion(self, name):
        """TODO: Docstring for analyze_funtion.

        :fuction_content_lines: TODO
        :returns: TODO
        """
        function_parameters = re.compile(
                '\s*((public|private)\s+)?(function|sub)\s+(\w+)\((.*)\)',
                re.IGNORECASE)
        if not self._functions[name]._analyzed:
            self._functions[name]._analyzed = True
            try:
                # parameters_string = function_parameters.match(
                parameters = function_parameters.match(
                        self._functions[name]._function_lines[0]).group(5)
                # parameters = analyze_funtion_param_definition(
                # parameters_string)
                # for variables in parameters:
                parameters = parameters.replace(' ', ',')
                for variables in parameters.split(","):
                    variables = variables.strip()
                    l_variables = variables.lower()
                    if l_variables not in ALL_KEYWORDS and \
                            l_variables not in \
                            self._declared_identifiers.keys() and \
                            l_variables != '':
                        self._declared_identifiers[l_variables] = \
                                IdentifierRepresentation(
                                        variables,
                                        self._functions[name].
                                        declaration_line_number,
                                        self._functions[name].
                                        _declaration_source_file,
                                        "identifiers")
                        self._unused_identifiers[l_variables] = \
                            IdentifierRepresentation(
                                variables, self._functions[name].
                                _declaration_line_number,
                                self._functions[name].
                                _declaration_source_file, "identifiers")
                self.parse_variables(
                        self._functions[name]._function_lines[1:],
                        self._functions[name]._declaration_source_file,
                        self._functions[name]._declaration_line_number + 1)
            except AttributeError:
                self.parse_variables(
                        self._functions[name]._function_lines[1:],
                        self._functions[name]._declaration_source_file,
                        self._functions[name]._declaration_line_number + 1)

    def analyze_funtion_param_definition(self, header):
        """TODO: Docstring for analyze_funtion_param_definition.

        :header: TODO
        :returns: TODO
        """
        pass

    def analyze_function_call_prams(self, arg1):
        """TODO: Docstring for analyze_function_call_prams.

        :arg1: TODO
        :returns: TODO

        """
        pass

    def return_value_of_expression(self, arg1, oper, arg2):
        """Function takes two operands and operator to compute result of
        expression

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

    def analyze_identifier_reference(self, word):
        """Function estimates all necessary states about identifier and
        triggers Error or Warnings.

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

    def evaluate_expression(self, string):
        """Function evaluates expression that is present in input string.

        @param string - contains expression
        @return: evaluated result of expression
            - #VALUE# - proper value
            - #NULL# - no return value (for example procedure call without
            return value instead of function call)
            - #MISS_OPE# - two values (identifiers of functions) are
            not correctly separated by operand (either operand is missing
            entirely or it has improper format)
            - #INVALID# - TODO
        """
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
        missing_operator_regex = re.compile(
                missing_operator_string, re.IGNORECASE)
        contains_invalid_regex = re.compile(
                contains_invalid_string, re.IGNORECASE)
        if string == "":
            return ""
        elif single_value_regex.match(string):
            single_value_match = single_value_regex.match(string)
            return self.analyze_identifier_reference(
                    single_value_match.group(1))

        elif evaluation_regex.match(string):
            evaluation_match = evaluation_regex.match(string)
            print('"{0}", "{1}", "{2}"'.format(
                evaluation_match.group(1), evaluation_match.group(4),
                evaluation_match.group(5)))
            arg1 = self.analyze_identifier_reference(evaluation_match.group(1))
            if evaluation_match.group(4):
                operator = self.analyze_identifier_reference(
                    evaluation_match.group(4))
            else:
                operator = ""
            arg2 = self.analyze_identifier_reference(evaluation_match.group(5))
            string = self.return_value_of_expression(arg1, operator, arg2)

            if evaluation_match.group(8):
                return self.evaluate_expression(
                        string + evaluation_match.group(8))
            else:
                return string
        elif contains_invalid_regex.match(string):
            return INVALID
        elif missing_operator_regex.match(string):
            return MISS_OPE
        else:
            ipdb.set_trace()  # #BREAKPOINT#

    def process_inner_function_prototype(
            self, function_string, position, name_space, function_name=""):
        """TODO: Docstring for process_inner_function_prototype.

        :function_string: TODO
        :position: TODO
        :name_space: TODO
        :functin_name: TODO
        :returns: TODO

        """
        print('process_inner_function_prototype: "{0}"'.format(
            function_string))
        list_of_parameters = list()
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
            evaluated_parameter = self.evaluate_expression(parameter)
            if evaluated_parameter == VALUE:
                list_of_parameters.append(VALUE)

            elif evaluated_parameter == NULL:
                parameters_correct = False
                list_of_parameters.append(NULL)

            elif evaluated_parameter == INVALID:
                parameters_correct = False
                list_of_parameters.append(INVALID)

            elif evaluated_parameter == MISS_OPE:
                parameters_correct = False
                list_of_parameters.append(MISS_OPE)

        if parameters_correct:
            if object_name != "":
                result = self.analyze_method(
                        object_name, fun_name, list_of_parameters)
            else:
                result = self.analyze_function(fun_name, list_of_parameters)
            return result
        else:
            return INVALID

    def analyze_method(self, object_name, method_name, list_of_parameters):
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

    def analyze_function(self, fun_name, list_of_parameters):
        """Anlyzes function call defined by function name. list_of_parameters
        is used to determined if the function definition is corrsponding to
        number of parameters that this function is called with.

        @param fun_name TODO
        @param list_of_parameters TODO
        @return:
            - #VALUE# - normal return
            - #NULL# - no return value (in case of Sub)
            - #INVALID# - wrong function paramters
        """
        return VALUE

    def analyze_and_evaluate_reference_side(
            self, function_string, position, name_space, function_name=""):
        """ Function is called on string that might contain function call. In
        case that regex which is designed to fined most inner brace in
        expression finds pattern that describes function call it is analyzed
        by function process_inner_function_prototype.

        :function_string: TODO
        :position: TODO
        :name_space: TODO
        :function_name: TODO
        :returns: TODO
        """
        print('analyze_and_evaluate_reference_side: "{0}"'.format(
            function_string))
        inner_fun_regx = re.compile(
            r'(((\b[a-zA-Z]\w+\b)\.)?((\b[a-zA-Z]\w+\b)\s*\(([^()]*)\)))',
            re.IGNORECASE)

        while inner_fun_regx.search(function_string):
            m = inner_fun_regx.search(function_string)
            begin = m.start(1)
            end = m.end(1)
            function_result = self.process_inner_function_prototype(
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

        return self.evaluate_expression(function_string)

    def identifier_changing(
            self, name, line_number, file_name, namespace, namespace_name=""):
        """TODO:

        @param name TODO
        @param line_number TODO
        @param file_name TODO
        @param namespace TODO
        @param namespace_name TODO
        @return: TODO

        """
        pass

    def identifier_referencing(
            self, name, line_number, file_name, namespace, namespace_name=""):
        """TODO:

        @param name TODO
        @param line_number TODO
        @param file_name TODO
        @param namespace TODO
        @param namespace_name TODO
        @return: TODO

        """
        pass

    def identifier_changing_function(
            self, name, function_name, line_number, file_name):
        """TODO:

        @param name TODO
        @param function_name TODO
        @param line_number TODO
        @param file_name TODO
        @return: TODO

        """
        pass

    def identifier_changing_method(
            self, name, method_name, line_number, file_name):
        """TODO: Docstring for identifier_changing_method.

        @param name TODO
        @param method_name TODO
        @param line_number TODO
        @param file_name TODO
        @return: TODO

        """
        pass


########################################
# list of possible syntactical objects #
########################################

# global_namespace

# if_condition

# for_loop

# while_loop

# switch_case

# function_block

# class_block

# class_method_block

# declaration

# assignment

# reference

# built_in_function_reference

# user_defined_function_reference
