# Author: Ondrej Zapletal
# Date: 2016-01-29
# Description:

HELP_STRING = "usage: TATS_Syntax_Checker [file name | flags] [args]\n\n" \
    "flags:\n --version(-v) : returns version\n --help(-h)    :" \
    " shows this help\n\n\nargs:\n0 ('') : show only error in this file" \
    "\n1       : show errors in all files within project "

NAME = "TATS syntax checker"

VERSION = "Alpha 0.0"

AUTHOR = "Ondrej Zapletal"

DATE = "1/13/2016"

# -----------------------------------------------------------------------------

ARITHMETIC_OPERATORS = ['\*', '\/', '\+', '-', 'mod', '\&', r'\\', '\^']

ASSIGNMENT_OPERATORS = ['=']

COMPARISON_OPERATORS = ['=', '<>', '<', '>', '<=', '>=', 'is']

CONCATENATION_OPERATORS = ['\&', '\+']

LOGICAL_OPERATORS = ['xor', 'or', 'and', 'imp', 'eqv', 'not']

VALUE = "#VALUE#"

NULL = "#NULL#"

OPERATOR = "#OPERATOR#"

INVALID = "#INVALID#"

MISS_OPE = "#MISSING_OPERATOR#"

MISS_CLS = "#MISSING_CLOSING#"

MISS_OPN = "#MISSING_OPENING#"

IDENTIFIER = '(".*?"|&\w+|\w+|[+-]?\d+(\.\d+)?)'

GLOBAL = 0

FUNCTION = 1

CLASS = 2

METHOD = 3

SINGLE_KEYWORD_ON_LINE = []


SPECIAL_KEYWORDS = [
    'AddMonitor', 'AddRangeWatch',  'AddRead', 'AddWatch',  'AddWrite', 'Beep',
    'BeginDrive', 'BeginGroup',  'CheckItem', 'Delay',  'EndDrive', 'EndGroup',
    'GetAtsProperty', 'GetEnumeration',  'Halt', 'InspectItem', 'ItemBitCount',
    'ItemDataType',   'ItemDescription',  'ItemEnumerations',   'ItemMaxValue',
    'ItemMinValue',  'ItemMode',  'ItemName', 'ItemNodeLevel',  'ItemNodeType',
    'ItemRate',   'ItemResolution',  'ItemSize',   'ItemUnits',  'MonitorSync',
    'Output',    'Pane',   'Prompt',    'PromptInput',   'Read',    'ReadEnum',
    'ReadMonitor',   'RemoveMonitor',  'TriggerGroup',   'UserDebug',  'Write',
    'WriteEnum'
]

TATS_CONSTANTS = [
    'Empty',              'False',              'Nothing',              'Null',
    'ScriptEngine',   'ScriptEngineBuildVersion',   'ScriptEngineMajorVersion',
    'ScriptEngineMinorVersion',       'True',      'atsAll',       'atsCancel',
    'atsClearMonitor',           'atsClearOutput',           'atsClearProject',
    'atsClearUserDebug', 'atsEqual', 'atsFail', 'atsForever', 'atsGreaterThan',
    'atsGreaterThanOrEqual',    'atsGroup',    'atsHalt',    'atsHostComputer',
    'atsHostName',   'atsHostVersion',  'atsInRange',   'atsInfo',  'atsInput',
    'atsLessThan',      'atsLessThanOrEqual',      'atsNo',      'atsNotEqual',
    'atsOk',    'atsOutOfRange',     'atsPass',    'atsPassFail',    'atsRamp',
    'atsReceive',  'atsSawtooth', 'atsServerComputer',  'atsServerFramePeriod',
    'atsServerVersion',  'atsShowMonitor',  'atsShowOutput',  'atsShowProject',
    'atsShowUserDebug',     'atsSinusoid',     'atsStep',     'atsStepDoublet',
    'atsSyncError',     'atsTransceive',      'atsTransmit',     'atsTriangle',
    'atsUsername',       'atsYes',      'atsYesNo',       'vbAbortRetryIgnore',
    'vbApplicationModal',     'vbArray',      'vbBinaryCompare',     'vbBlack',
    'vbBlue',   'vbBoolean',   'vbByte',    'vbCr',   'vbCrLf',   'vbCritical',
    'vbCurrency',  'vbCyan',   'vbDataObject',  'vbDatabaseCompare',  'vbDate',
    'vbDecimal',  'vbDefaultButton1',  'vbDefaultButton2',  'vbDefaultButton3',
    'vbDefaultButton4',  'vbDouble',   'vbEmpty',  'vbError',  'vbExclamation',
    'vbFirstFourDays',    'vbFirstFullWeek',    'vbFirstJan1',    'vbFormFeed',
    'vbFriday',   'vbGeneralDate',  'vbGreen',   'vbInformation',  'vbInteger',
    'vbLf',  'vbLong',  'vbLongDate',  'vbLongTime',  'vbMagenta',  'vbMonday',
    'vbNewLine', 'vbNo', 'vbNull',  'vbNullChar', 'vbNullString', 'vbOKCancel',
    'vbOKOnly',    'vbObject',    'vbObjectError',    'vbQuestion',    'vbRed',
    'vbRetryCancel',  'vbSaturday',  'vbShortDate', 'vbShortTime',  'vbSingle',
    'vbString',   'vbSunday',    'vbSystemModal',   'vbTab',   'vbTextCompare',
    'vbThursday',    'vbTuesday',     'vbUseSystem',    'vbUseSystemDayOfWeek',
    'vbVariant',   'vbVerticalTab',   'vbWednesday',   'vbWhite',   'vbYellow',
    'vbYes', 'vbYesNo', 'vbYesNoCancel'
]

TATS_FUNCTIONS = [
    'Abs',   'AddRangeWatch',  'AddRead',   'AddWatch',  'AddWrite',   'Array',
    'Asc',   'AscB',  'AscW',   'Atn',  'CBool',   'CByte',  'CCur',   'CDate',
    'CDbl',  'CInt',  'CLng',  'CSng',   'CStr',  'CheckItem',  'Chr',  'ChrB',
    'ChrW', 'Cos',  'CreateObject', 'Date', 'DateAdd',  'DateDiff', 'DatePart',
    'DateSerial',   'DateValue',  'Day',   'Eval',   'Exp',  'Filter',   'Fix',
    'FormatCurrency',   'FormatDateTime',    'FormatNumber',   'FormatPercent',
    'GetAtsProperty',  'GetEnumeration',  'GetLocale',  'GetObject',  'GetRef',
    'Hex',  'Hour',   'InStr',  'InStrB',  'InStrRev',   'InspectItem',  'Int',
    'IsArray',   'IsDate',   'IsEmpty',  'IsNull',   'IsNumeric',   'IsObject',
    'ItemBitCount',   'ItemDataType',  'ItemDescription',   'ItemEnumerations',
    'ItemMaxValue',  'ItemMinValue',  'ItemMode', 'ItemName',  'ItemNodeLevel',
    'ItemNodeType',  'ItemRate',   'ItemResolution',  'ItemSize',  'ItemUnits',
    'Join',  'LBound',  'LCase',  'LTrim',   'Left',  'LeftB',  'Len',  'LenB',
    'LoadPicture',  'Log',  'Mid',   'MidB',  'Minute',  'Month',  'MonthName',
    'Now',  'Oct', 'RGB',  'RTrim', 'ReadEnum',  'Replace', 'Right',  'RightB',
    'Rnd',  'Round', 'Second',  'SetLocale',  'Sgn',  'Sin', 'Space',  'Split',
    'Sqr', 'StrComp',  'StrReverse', 'Tan', 'Time',  'TimeSerial', 'TimeValue',
    'Timer', 'TriggerGroup', 'Trim',  'TypeName', 'UBound', 'UCase', 'VarType',
    'Weekday', 'WeekdayName', 'WriteEnum', 'Year'
]

TATS_KEYWORDS = [
    'AddMonitor', 'Beep', 'BeginDrive', 'BeginGroup', 'ByRef', 'ByVal', 'Call',
    'Case', 'Class',  'Const', 'Delay', 'Dim', 'Do',  'Each', 'Else', 'ElseIf',
    'End',   'EndDrive',  'EndGroup',   'Erase',  'Err',   'Error',  'Execute',
    'ExecuteGlobal', 'Exit',  'Explicit', 'For', 'Foreach',  'Function', 'Get',
    'Halt',  'If',  'In',  'InputBox',   'Let',  'Loop',  'Me',  'MonitorSync',
    'MsgBox',  'New', 'Next',  'On',  'Option',  'Output', 'Pane',  'Preserve',
    'Private',  'Prompt',  'PromptInput',  'Property',  'Public',  'Randomize',
    'ReDim', 'Read', 'ReadMonitor', 'Rem', 'RemoveMonitor', 'Resume', 'Select',
    'Set',  'Step', 'Stop',  'String',  'Sub', 'Then',  'To', 'Until',  'Wend',
    'While', 'With', 'Write'
]

ALL_KEYWORDS = TATS_CONSTANTS + TATS_FUNCTIONS + TATS_KEYWORDS

ALL_OPERATORS = ARITHMETIC_OPERATORS + ASSIGNMENT_OPERATORS + \
    COMPARISON_OPERATORS + CONCATENATION_OPERATORS + LOGICAL_OPERATORS

ALL_KEYWORDS = list(set(ALL_KEYWORDS))

EVALUATING_OPERATORS = "({0})".format('|'.join(ALL_OPERATORS))

ALL_OPERATORS = list(set(ALL_OPERATORS))
