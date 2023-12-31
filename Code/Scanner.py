from Code import Util


class Scanner:
    STATES = {
        'START': False,
        'IN_COMMENT': False,
        'IN_IDENTIFIER': False,
        'IN_NUMBER': False,
        'IN_ASSIGN': False,
        'DONE': False,
        'OTHER': False
    }
    KEYWORDS = ['else', 'end', 'if', 'repeat', 'then', 'until', 'read', 'write']
    OPERATORS = {
        '+': 'Plus',
        '-': 'Minus',
        '*': 'Mult',
        '/': 'Div',
        ':': 'Colon',
        '=': 'Equal',
        ':=': 'Assign',
        '>': 'Greater',
        '<': 'Lessthan',
        ';': 'Semicolon',
        '(': 'OpenBracket',
        ')': 'ClosedBracket'
    }

    # initialize states and set the current state to start.
    def __init__(self):
        self.change_current_state('START')
        self.tokens = []
        self.state_other = False

    # set the current state to true and other states to false (transition from the current state to another).
    def change_current_state(self, state):
        for key in self.STATES:
            self.STATES[key] = False
        self.STATES[state] = True

    # check if this is the current state.
    def check_state(self, state):
        return self.STATES[state]

    # scan the input file character by character,
    # where each character where each transition is made based on the current state and the input character.
    # Ex: if we are in the start state, and we find a '{' we transition to the comment state.

    def tokenize(self, input_file):
        input_text = Util.get_file_text(input_file)
        token = ''
        for c in input_text:
            if self.check_state('START'):
                if Util.is_symbol(c):
                    self.change_current_state('DONE')
                elif c == ' ':
                    continue
                elif c == '{':
                    self.change_current_state('IN_COMMENT')
                elif Util.is_num(c):
                    self.change_current_state('IN_NUMBER')
                elif Util.is_str(c):
                    self.change_current_state('IN_IDENTIFIER')
                elif Util.is_col(c):
                    self.change_current_state('IN_ASSIGNMENT')

            elif self.check_state('IN_COMMENT'):
                if c == '}':
                    self.change_current_state('DONE')
                else:
                    self.change_current_state('IN_COMMENT')

            elif self.check_state('IN_NUMBER'):
                if Util.is_num(c):
                    self.change_current_state('IN_NUMBER')
                elif c == ' ':
                    self.change_current_state('DONE')
                else:
                    self.change_current_state('OTHER')

            elif self.check_state('IN_IDENTIFIER'):
                if Util.is_str(c):
                    self.change_current_state('IN_IDENTIFIER')
                elif c == ' ':
                    self.change_current_state('DONE')
                else:
                    self.change_current_state('OTHER')

            elif self.check_state('IN_ASSIGNMENT'):
                if c == '=':
                    self.change_current_state('DONE')
                else:
                    self.change_current_state('OTHER')

            if not self.check_state('OTHER'):
                token += c

            if self.check_state('OTHER'):
                self.change_current_state('DONE')
                self.state_other = True

            if self.check_state('DONE'):
                self.classify(token)
                if self.state_other:
                    token = c
                    if Util.is_col(c):
                        self.change_current_state('IN_ASSIGNMENT')
                    if Util.is_comment(c):
                        self.change_current_state('IN_COMMENT')
                    if Util.is_num(c):
                        self.change_current_state('IN_NUMBER')
                    if Util.is_str(c):
                        self.change_current_state('IN_IDENTIFIER')
                    if Util.is_symbol(c):
                        self.classify(c)
                        token = ''
                        self.change_current_state('START')
                    self.state_other = False
                else:
                    token = ''
                self.change_current_state('START')
        return self.tokens

    # classify each token to its type in a dictionary (will be later used in formatting the output).
    def classify(self, token):
        if token[-1:] == ' ':
            token = token[0:-1]
        if Util.is_str(token):
            if token in self.KEYWORDS:
                self.tokens.append([token, token.upper()])
            else:
                self.tokens.append([token, 'IDENTIFIER'])
        elif Util.is_num(token):
            self.tokens.append([token, 'NUMBER'])
        elif token in self.OPERATORS:
            self.tokens.append([token, self.OPERATORS[token].upper()])
        # elif is_comment(token):
        #     self.tokens.append([token[1:len(token)-1], 'Comment'])

    # export data to an output file
    def export(self):
        with open('Tokens.txt', 'w') as f:
            for token in self.tokens:
                f.write('{:}, {:}\n'.format(token[0], token[1]))
