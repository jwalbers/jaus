import sys
from pygments import highlight

from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.formatters import get_all_formatters, get_formatter_by_name, \
     get_formatter_for_filename, find_formatter_class, \
     TerminalFormatter
from pygments.token import Name, Keyword

from pygments.formatters.rtf import RtfFormatter
from pygments.styles import get_style_by_name

def highlight2rtf(ifname, ofname):
    f = file( ifname, 'rb')
    code = f.read()
    f.close()
    outf = file( ofname, 'w')
    lexer = get_lexer_by_name('xml')
    fmter = RtfFormatter(fontface='Consolas',style=get_style_by_name('emacs'))
    highlight(code,lexer,fmter,outf)
    outf.close()

if __name__ == '__main__':

    ifname = sys.argv[1]
    if ifname[-4:] == '.xml':
        rtfname = ifname[:-4]+'.rtf'
        highlight2rtf(sys.argv[1], rtfname);
