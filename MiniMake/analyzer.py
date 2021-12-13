from sly import Lexer, Parser
class MakeLexer(Lexer):

    tokens = {COMMAND, COLON, NEWLINE, CONDITION, TARGET, SPACE}

    ignore_comment = r'\#.*'


    TARGET = r'(\w+[.\w]+(?=:))'
    CONDITION = r'(?<=: )([\w. ]+)'
    NEWLINE = r'([\n])+|([\r][\n])+'
    SPACE = r'[\t ]+'
    COMMAND = r'[@+*a-zA-Zа-яА-Я_ \-\.\,\'\"!]+'
    COLON = r':'

class MakeParser(Parser):

    tokens = MakeLexer.tokens
  
    def __init__(self):
        self.names = { }

    @_('line NEWLINE lines')
    def lines(self, p):
        return [p.line] + p.lines

    @_('line')
    def lines(self, p):
        return [p.line]

    @_('')
    def lines(self, p):
        return []

    @_('target')
    def line(self, p):
        return p.target

    @_('command')
    def line(self, p):
        return p.command

    @_('TARGET COLON SPACE CONDITION')
    def target(self, p):
        return {p.TARGET : p.CONDITION.split(' ')}

    @_('TARGET COLON')
    def target(self, p):
        return {p.TARGET : []}

    @_('SPACE COMMAND')
    def command(self, p):
        return p.COMMAND

def analyzeData(data):    
    lexer = MakeLexer()
    parser = MakeParser()
    # тестовая печать
    # for token in lexer.tokenize(data):
    #     print(token)

    lines = parser.parse(lexer.tokenize(data))
    # тестовая печать
    # for line in lines:
        # print(line)

    return lines