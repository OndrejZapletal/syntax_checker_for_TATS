# Author: Ondrej Zapletal
# Date: 2016-01-29
# Description:


class IdentifierRepresentation(object):
    """Docstring for IdentifierRepresentation. """

    def __init__(
            self, name, decleration_line_number, decleration_source_file,
            identifier_type
                ):
        """TODO: to be defined1.

        :name: TODO
        """
        self._name = name
        self._declaration_source_file = decleration_source_file
        self._declaration_line_number = decleration_line_number
        self._identifier_type = identifier_type


class FunctionRepresentation(object):
    """Docstring for FunctionRepresentation. """

    def __init__(
            self, name, declaration_line_number, declaration_source_file,
            function_lines, procedure, private):
        """TODO: to be defined1.

        :name: TODO
        :source_file: TODO
        :declaration_line: TODO
        :function_line: TODO
        """
        # name of function
        self._name = name

        # name of file that contiain its definition
        self._declaration_source_file = declaration_source_file

        # line number in file whre declarataion starts
        self._declaration_line_number = declaration_line_number

        # list of lines that are consist entire function source code
        self._function_lines = function_lines

        # declared identifiers - list of identifiers that have been declared in
        # global name space.
        self._declared_identifiers = {}

        # unassigned identifiers - list of identifiers that have been declared
        # in global name space but never assigned any value
        self._unassigned_identifiers = {}

        # unassigned used identifiers - list of identifiers that have been
        # declared in global name space, never assigned any value, but used.
        self._unassigned_used_identifiers = {}

        # unused identifiers - list of identifiers that have been declared and
        # assigned in global name space but never used.
        self._unused_identifiers = {}

        # undeclared identifiers - list of identifiers that haven't been
        # declared in global name space. This means that they are not declared
        # as variable nor constant nor as a function.
        self._undeclared_identifiers = {}

        self._function_paramters = {}

        # if it Function or Sub
        self._procedure = procedure

        # function defined as private
        self._private = private

        # wheter function was ever analyzed
        self._analyzed = False

        # wheter function was ever called
        self._called = False


class MethodRepresentation(object):
    """Docstring for MethodRepresentation. """

    def __init__(
            self, name, declaration_line_number, decleration_source_file,
            method_lines, class_name, procedure, private):
        """TODO: to be defined1.

        :name: TODO
        :declaration_line_number: TODO
        :decleration_source_file: TODO
        :function_lines: TODO
        :class_name: TODO
        """
        self._name = name
        self._declaration_line_number = declaration_line_number
        self._declaration_source_file = decleration_source_file
        self._method_lines = method_lines
        self._class_name = class_name
        self._declared_identifiers = {}
        self._undeclared_identifiers = {}
        self._unused_identifiers = {}
        self._procedure = procedure
        self._private = private
        self._analyzed = False
        self._called = False


class ClassRepresentation(object):
    """Docstring for ClassRepresentation. """

    def __init__(
            self, name, declaration_line_number, declaration_source_file,
            class_lines):
        """TODO: to be defined1.

        :name: TODO
        :declaration_line_number: TODO
        :declaration_source_file: TODO
        :class_lines: TODO
        """
        self._name = name
        self._declaration_line_number = declaration_line_number
        self._declaration_source_file = declaration_source_file
        self._class_lines = class_lines
        self._class_methods = {}
        self._declared_identifiers = {}
        self._undeclared_identifiers = {}
        self._unused_identifiers = {}
        self._class_instantiated = False
        self._analyzed = False


class DefectRepsentation(object):
    """Docstring for DefectRepsentation. """

    def __init__(self, name, error_type, source_file, line_number):
        """TODO: to be defined1.

        :error_type: TODO
        :error_description: TODO
        :source_file: TODO
        :line_number: TODO
        """
        self._name = name
        self._error_type = error_type
        if error_type == "Unused Function":
            self._error_description = error_type + ': ' + name + \
                    " - since this function is never called" \
                    " it couldn't be properly analyzed"
        else:
            self._error_description = error_type + ': ' + name
        self._source_file = source_file
        self._line_number = line_number
