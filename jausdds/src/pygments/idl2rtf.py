import sys
from pygments import highlight

from pygments.lexers import JavascriptLexer
from pygments.formatters import get_all_formatters, get_formatter_by_name, \
     get_formatter_for_filename, find_formatter_class, \
     TerminalFormatter
from pygments.token import Name, Keyword

class MyLexer(JavascriptLexer):
     # In JS, interface is Keyword.Reserved
     RESERVED_KEYWORDS = [ 'oneway', 'in', 'struct', 'enum', 'module', 'valuetype', 'sequence'  ]
     PSEUDO_KEYWORDS = [ 'Real', 'NaturalNumber', 'UCS', 'TBD' ] 

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
    lexer = MyLexer()
    fmter = RtfFormatter(fontface='Consolas',style=get_style_by_name('emacs'))
    highlight(code,lexer,fmter,outf)
    outf.close()


if __name__ == '__main__':

    ifname = sys.argv[1]
    if ifname[-4:] == '.idl':
        rtfname = ifname[:-4]+'.rtf'
        highlight2rtf(sys.argv[1], rtfname);
