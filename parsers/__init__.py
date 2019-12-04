# Named as `parsers` because `parser` will produce ImportError due to conflict with internal `parser.py` file

from parsers.css_parser import *
from parsers.wiki_parser import *

__all__ = ['css_parser', 'wiki_parser']
