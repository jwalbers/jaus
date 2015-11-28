import sys
from pygments import highlight

from pygments.lexers import JavascriptLexer
from pygments.formatters import get_all_formatters, get_formatter_by_name, \
     get_formatter_for_filename, find_formatter_class, \
     TerminalFormatter
from pygments.token import Name, Keyword

class JausLexer(JavascriptLexer):
     # In JS, interface is Keyword.Reserved
     PRIMITIVE_TYPES = [ 'uint8', 'uint16', 'uint24', 'uint32','uint64',
                         'int8', 'int16', 'int32', 'int64',
                         'float', 'double', 'string', 'vstring']
     UNIT_KEYWORDS = [
            'meter', 'kilogram', 'second', 'ampere', 'kelvin', 'mole', 'candela', 
            # derived units
            'square_meter', 'cubic_meter', 'meter_per_second', 'meter_per_second_squared', 
            'reciprocal_meter', 'kilogram_per_cubic_meter', 'cubic_meter_per_kilogram', 
            'ampere_per_square_meter', 'ampere_per_meter', 'mole_per_cubic_meter', 
            'candela_per_square_meter', 'one', 

            # derived units with special names and symbols
            'radian', 'steradian', 'hertz', 'newton', 'pascal', 'joule', 'watt', 
            'coulomb', 'volt', 'farad', 'ohm', 'siemens', 'weber', 'tesla', 'henry', 
            'degree_Celsius', 'lumen', 'lux', 'becquerel', 'sievert', 'katal', 
            'pascal_second', 'newton_meter', 'newton_per_meter', 'radian_per_second', 
            'radian_per_second_squared', 'watt_per_square_meter', 'joule_per_kelvin', 
            'joule_per_kilogram', 'watt_per_meter_kelvin', 
            'joule_per_cubic_meter', 'volt_per_meter', 'coulomb_per_cubic_meter', 
            'coulomb_per_square_meter', 'farad_per_meter', 'henry_per_meter', 
            'joule_per_mole', 'joule_per_mole_kelvin', 'coulomb_per_kilogram', 
            'gray_per_second', 'watt_per_square_meter_steradian', 'katal_per_cubic_meter', 

            # Non-SI units accepted for use with the International System
            # 'second' is already SI, 

            'minute', 'hour', 'day', 'degree', 'liter', 'metric ton', 
            'neper', 'bel', 'nautical mile', 'knot', 'are', 'hectare', 'bar', 'angstrom', 
            'barn', 'curie', 'roentgen', 'rad', 'rem',

            # JAUS relevant units
            'percent', 'pixel', 'frame', 'frames_per_second', 'millisecond', 'month', 'year',
            'milliradian', 'milliradian_per_second',
            'millimeter', 'millimeter_per_second' ]

     RESERVED_KEYWORDS = [ 'service', 'references', 'messages', 'query', 'inform', 'command', 'description', 'assumptions', 'inherits_from',
                           'record', 'sequence', 'variant', 'list', 'bit_field',
                           'events', 'protocol', 'start', 'state', 'state_machine', 'initial']
     PSEUDO_KEYWORDS = PRIMITIVE_TYPES + UNIT_KEYWORDS + [ 'required', 'optional', 'repeated' ]

     def get_tokens_unprocessed(self, text):
         # Munge tokens for IDL
         for index, token, value in JavascriptLexer.get_tokens_unprocessed(self, text):
             if value.find('UCS') != -1:
                 # print 'UCS is a %s'%(repr(token))
                 pass
             if value.find('@') != -1:
                 # @ is a Token.Error, need to extend lexer to recognize
                 # annotations?
                 # print '%s is a %s'%(value,repr(token))
                 pass
             if token is Name.Other and value in self.RESERVED_KEYWORDS:
                 yield index, Keyword.Reserved, value
             elif token is Name.Other and value in self.PSEUDO_KEYWORDS:
                 yield index, Keyword.Pseudo, value
             else:
                 yield index, token, value


from pygments.formatters.rtf import RtfFormatter
from pygments.styles import get_style_by_name

def highlight2rtf(ifname, ofname):
    f = file( ifname, 'rb')
    code = f.read()
    f.close()
    outf = file( ofname, 'w')
    lexer = JausLexer()
    fmter = RtfFormatter(fontface='Consolas',style=get_style_by_name('emacs'))
    highlight(code,lexer,fmter,outf)
    outf.close()

def print_usage():
     print "jaus2rtf.py <fname>.jaus"
     print "   Produce colored RTF in <fname>.rtf"
     
if __name__ == '__main__':

    arg1 = sys.argv[1]
    if arg1 in ['--help','-h']:
        print_usage()
    elif arg1[-5:] == '.jaus':
        rtfname = arg1[:-5]+'.rtf'
        highlight2rtf(sys.argv[1], rtfname);
    else:
        print "Unrecognized command line argument: %s"%arg1
        print_usage()
