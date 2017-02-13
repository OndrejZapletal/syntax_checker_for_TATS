import collections
import re

TATS_CONSTANTS = ['empty', 'false', 'nothing', 'null', 'scriptengine', 'scriptenginebuildversion', 'scriptenginemajorversion', 'scriptengineminorversion', 'true', 'atsall', 'atscancel', 'atsclearmonitor', 'atsclearoutput', 'atsclearproject', 'atsclearuserdebug', 'atsequal', 'atsfail', 'atsforever', 'atsgreaterthan', 'atsgreaterthanorequal', 'atsgroup', 'atshalt', 'atshostcomputer', 'atshostname', 'atshostversion', 'atsinrange', 'atsinfo', 'atsinput', 'atslessthan', 'atslessthanorequal', 'atsno', 'atsnotequal', 'atsok', 'atsoutofrange', 'atspass', 'atspassfail', 'atsramp', 'atsreceive', 'atssawtooth', 'atsservercomputer', 'atsserverframeperiod', 'atsserverversion', 'atsshowmonitor', 'atsshowoutput', 'atsshowproject', 'atsshowuserdebug', 'atssinusoid', 'atsstep', 'atsstepdoublet', 'atssyncerror', 'atstransceive', 'atstransmit', 'atstriangle', 'atsusername', 'atsyes', 'atsyesno', 'vbabortretryignore', 'vbapplicationmodal', 'vbarray', 'vbbinarycompare', 'vbblack', 'vbblue', 'vbboolean', 'vbbyte', 'vbcr', 'vbcrlf', 'vbcritical', 'vbcurrency', 'vbcyan', 'vbdataobject', 'vbdatabasecompare', 'vbdate', 'vbdecimal', 'vbdefaultbutton1', 'vbdefaultbutton2', 'vbdefaultbutton3', 'vbdefaultbutton4', 'vbdouble', 'vbempty', 'vberror', 'vbexclamation', 'vbfirstfourdays', 'vbfirstfullweek', 'vbfirstjan1', 'vbformfeed', 'vbfriday', 'vbgeneraldate', 'vbgreen', 'vbinformation', 'vbinteger', 'vblf', 'vblong', 'vblongdate', 'vblongtime', 'vbmagenta', 'vbmonday', 'vbnewline', 'vbno', 'vbnull', 'vbnullchar', 'vbnullstring', 'vbokcancel', 'vbokonly', 'vbobject', 'vbobjecterror', 'vbquestion', 'vbred', 'vbretrycancel', 'vbsaturday', 'vbshortdate', 'vbshorttime', 'vbsingle', 'vbstring', 'vbsunday', 'vbsystemmodal', 'vbtab', 'vbtextcompare', 'vbthursday', 'vbtuesday', 'vbusesystem', 'vbusesystemdayofweek', 'vbvariant', 'vbverticaltab', 'vbwednesday', 'vbwhite', 'vbyellow', 'vbyes', 'vbyesno', 'vbyesnocancel']

TATS_FUNCTIONS = ['abs', 'addrangewatch', 'addread', 'addwatch', 'addwrite', 'array', 'asc', 'ascb', 'ascw', 'atn', 'cbool', 'cbyte', 'ccur', 'cdate', 'cdbl', 'cint', 'clng', 'csng', 'cstr', 'checkitem', 'chr', 'chrb', 'chrw', 'cos', 'createobject', 'date', 'dateadd', 'datediff', 'datepart', 'dateserial', 'datevalue', 'day', 'eval', 'exp', 'filter', 'fix', 'formatcurrency', 'formatdatetime', 'formatnumber', 'formatpercent', 'getatsproperty', 'getenumeration', 'getlocale', 'getobject', 'getref', 'hex', 'hour', 'instr', 'instrb', 'instrrev', 'inspectitem', 'int', 'isarray', 'isdate', 'isempty', 'isnull', 'isnumeric', 'isobject', 'itembitcount', 'itemdatatype', 'itemdescription', 'itemenumerations', 'itemmaxvalue', 'itemminvalue', 'itemmode', 'itemname', 'itemnodelevel', 'itemnodetype', 'itemrate', 'itemresolution', 'itemsize', 'itemunits', 'join', 'lbound', 'lcase', 'ltrim', 'left', 'leftb', 'len', 'lenb', 'loadpicture', 'log', 'mid', 'midb', 'minute', 'month', 'monthname', 'now', 'oct', 'rgb', 'rtrim', 'readenum', 'replace', 'right', 'rightb', 'rnd', 'round', 'second', 'setlocale', 'sgn', 'sin', 'space', 'split', 'sqr', 'strcomp', 'strreverse', 'tan', 'time', 'timeserial', 'timevalue', 'timer', 'triggergroup', 'trim', 'typename', 'ubound', 'ucase', 'vartype', 'weekday', 'weekdayname', 'writeenum', 'year']

TATS_KEYWORDS = ['addmonitor', 'beep', 'begindrive', 'begingroup', 'byref', 'byval', 'call', 'case', 'class', 'const', 'delay', 'dim', 'do', 'each', 'else', 'elseif', 'end', 'enddrive', 'endgroup', 'erase', 'err', 'error', 'execute', 'executeglobal', 'exit', 'explicit', 'for', 'foreach', 'function', 'get', 'halt', 'if', 'in', 'inputbox', 'let', 'loop', 'me', 'monitorsync', 'msgbox', 'new', 'next', 'on', 'option', 'output', 'pane', 'preserve', 'private', 'prompt', 'promptinput', 'property', 'public', 'randomize', 'redim', 'read', 'readmonitor', 'rem', 'removemonitor', 'resume', 'select', 'set', 'step', 'stop', 'string', 'sub', 'then', 'to', 'until', 'wend', 'while', 'with', 'write']

Token = collections.namedtuple(
    'Token', ['typ', 'value', 'line', 'column', 'id'])

OPERATORS = [
    '-', '<', '<=', '<>', '=', '>', '>=', '\&', '\*', '\+', '\+', '\/', '\^',
    'and', '\beqv\b', '\bimp\b', '\bis\b', '\bmod\b', '\bnot\b', '\bor\b',
    '\bxor\b', r'\\'
    ]

OP = '|'.join(OPERATORS)


def tokenize(code):
    token_specification = [
        # Integer, decimal number or hexadecimal number
        ('NUMBER',   r'(&h[a-f0-9]+|\d+(\.\d*)?)'),
        ('STRING',   r'".*?"'),
        ('COMMENT',  r"'.*(?=\n)"),
        ('DOT',      r'\.'),
        ('OPEN_BRC', r'\('),
        ('CLOS_BRC', r'\)'),
        ('COMMA',    r','),
        ('COLON',    r':'),
        ('ASSIGN',   r'='),            # Assignment operator
        ('OP',       r'(%s)' % OP),    # Arithmetic operators
        ('ID',       r'[A-Za-z][A-Za-z0-9_]*'),    # Identifiers
        ('NEWLINE',  r'\n'),           # Line endings
        ('SKIP',     r'[ \t]+'),       # Skip over spaces and tabs
        ('BKN_LINE',  r'_\s*\n'),
        ('COMMENT_EOF',  r"'.*$"),
        ('MISMATCH', r'.'),            # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    condition_statement = False
    token_id = 0
    for mo in re.finditer(tok_regex, code, re.IGNORECASE):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            condition_statement = False
            column = mo.start() - line_start
            token_id += 1
            yield Token(kind, value, line_num, column, token_id)
        elif kind == 'SKIP' or kind == 'COMMENT' or kind == 'BKN_LINE':
            pass
        elif kind == 'ASSIGN' and condition_statement:
            kind = 'OP'
            column = mo.start() - line_start
            token_id += 1
            yield Token(kind, value, line_num, column, token_id)
        elif kind == 'MISMATCH':
            raise RuntimeError('%r unexpected on line %d' % (value, line_num))
        else:
            l_value = value.lower()
            if kind == 'ID' and (l_value == 'if' or l_value == 'elseif'):
                kind = 'KEYWORD'
                condition_statement = True
            elif kind == 'ID' and l_value in TATS_KEYWORDS:
                kind = 'KEYWORD'
            elif kind == 'ID' and l_value in TATS_FUNCTIONS:
                kind = 'FUNCTION'
            elif kind == 'ID' and l_value in TATS_CONSTANTS:
                kind = 'CONSTANT'
            column = mo.start() - line_start
            token_id += 1
            yield Token(kind, value, line_num, column, token_id)


def statements_extractions(source):
    statement = []
    consec_new_line = False
    for token in tokenize(source):
        if token.typ == "NEWLINE" and not consec_new_line:
            consec_new_line = True
            yield statement
            statement = []
        if token.typ == "NEWLINE" and consec_new_line:
            pass
        else:
            statement.append(token)
            consec_new_line = False
