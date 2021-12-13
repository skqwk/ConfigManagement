
from sly import Lexer, Parser
import json
import codecs
import sys

class ConfLexer(Lexer):

    tokens = {NUMBER, STRING, LPAR, RPAR, ASSIGN, NAME, LCODE, RCODE, SEMICOLON, POINTER, FOR, PATTERN}

    ignore = '\t\r '
    ignore_newline = r'\n+'
    ignore_comment = r'\#.*'

    SEMICOLON = r';'
    STRING = r'\"[\w\dа-яА-Я_\-\.\,\s]+\"'
    LPAR = r'\('
    RPAR = r'\)'
    ASSIGN = r'='
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]+'
    POINTER = r'&'
    LCODE = r'\{'
    RCODE = r'\}'
    NUMBER = r'\d+'

    NAME["for"] = FOR
    PATTERN = r'\"[\w\dа-яА-Я_\-\.\,\s]+&[\w\dа-яА-Я_\-\.\,\s]*\"'

    # предобработка токена
    @_(r'\d+')
    def NUMBER(self, t):
      t.value = int(t.value)
      return t

class ConfParser(Parser):

  tokens = ConfLexer.tokens
  
  def __init__(self):
    self.names = { }

  # program ::= { statements } object
  @_('LCODE statements RCODE object')
  def program(self, p):
    return p.object

  # object ::= ( list_assign ) 
  @_('LPAR list_assign RPAR')
  def object(self, p):
    d = {}
    d.update(p.list_assign)
    return d

  # list_assign ::= assign list_assign |
  @_('assign list_assign')
  def list_assign(self, p):
      d = {}
      d.update(p.assign)
      d.update(p.list_assign)
      return d

  @_('')
  def list_assign(self, p):
    return {}

  # assign ::= NAME(value)
  @_('NAME LPAR list_value RPAR')
  def assign(self, p):
      d = {}
      d[p.NAME] = p.list_value
      return d

  # list_value ::= value list_value | 
  @_('value list_value')
  def list_value(self, p):
    if (isinstance(p.list_value, list)):
      if (len(p.list_value) != 0):
        return [p.value] + p.list_value
      return p.value  
    return [p.value] + [p.list_value]

  @_('')
  def list_value(self, p):
    return []


  # value ::= object | string | number | &NAME | for(b e s) | for(b e s PATTERN)
  @_('NUMBER')
  def value(self, p):
    return p.NUMBER
  
  @_('STRING')
  def value(self, p):
    s = p.STRING
    s = s[1:-1]
    return s

  @_('object')
  def value(self, p):
    return p.object 
  
  @_('POINTER NAME')
  def value(self, p):
        try:
            return self.names[p.NAME]
        except LookupError:
            print(f'Undefined name {p.NAME!r}')
            return 0

  @_('FOR LPAR NUMBER NUMBER NUMBER RPAR')
  def value(self, p):
      b = p.NUMBER0
      e = p.NUMBER1
      s = p.NUMBER2
      a = []
      for x in range(b, e, s):
          a.append(x)
      return a

  @_('FOR LPAR NUMBER NUMBER NUMBER PATTERN RPAR')
  def value(self, p):
      b = p.NUMBER0
      e = p.NUMBER1
      s = p.NUMBER2
      word = p.PATTERN
      word = word[1:-1]
      parts = word.split('&')
      a = []
      for x in range(b, e, s):
          a.append(parts[0]+str(x)+parts[1])
      return a

  # statements ::= statement statements |
  @_('statement statements')
  def statements(self, p):
    p.statement
    p.statements
  
  @_('')
  def statements(self, p):
    pass
  
  # statement ::= NAME=list_value;
  @_('NAME ASSIGN list_value SEMICOLON')
  def statement(self, p):
      self.names[p.NAME] = p.list_value
  
def main():
    f = codecs.open( sys.argv[1], "r", "utf-8" )
    data = f.read()
    lexer = ConfLexer()
    parser = ConfParser()
    result = parser.parse(lexer.tokenize(data))
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

main()