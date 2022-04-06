from collections import namedtuple
from typing import List

Token = namedtuple("Token", ["token_tag", "value"])


class Scanner:
    def __init__(self):
        self.parsed_tokens: List[Token] = []
        self.unparsed_characters: List[str] = []

        self.parenthesis_ratio = 0

    def scan_file(self, path: str):
        with open(path, "r") as fin:
            characters = [
                character for character in next(fin) if not character.isspace()
            ]

        for idx, character in enumerate(characters):
            self.scan(character, idx)

        if len(self.unparsed_characters) > 0:
            if self.unparsed_characters[-1] == "-":
                raise Exception(
                    f"{self.unparsed_characters[-1]} cannot be placed at the end of an expression!"
                )
            else:
                self.parseUnparsedCharacters()

        # not enough closing parenthesis
        if self.parenthesis_ratio:
            raise Exception(
                f"Opened parenthesis have not been closed at index {len(characters)}!"
            )

        # last char is sign
        if self.parsed_tokens[-1].value in ("-", "+", "*", "/", "="):
            raise Exception(
                f"{self.parsed_tokens[-1].value} cannot be placed at the end of an expression"
            )

    def scan(self, character: str, index: int):
        if character.isnumeric():
            self.scanNumeric(character, index)
        elif character.isalpha():
            self.scanVariable(character, index)
        elif character == "-":
            self.scanSubtraction(index)
        elif character == "+":
            self.scanAddition(index)
        elif character == "*":
            self.scanMultiplication(index)
        elif character == "/":
            self.scanDivision(index)
        elif character == "(":
            self.scanOpenParenthesis(index)
        elif character == ")":
            self.scanCloseParenthesis(index)
        elif character == "=":
            self.scanEquals(index)
        else:
            raise Exception(f'Unknown character at index {index}')


    def scanNumeric(self, numeric_character: str, index: int):
        if len(self.parsed_tokens) > 0:
            if self.parsed_tokens[-1].value == ")":
                raise Exception(
                    f"Cannot place an integer after a closed parenthesis at index {index}"
                )
            if self.parsed_tokens[-1].token_tag == 'variable':
                raise Exception(
                    f"Cannot place an integer after a variable at index {index}"
                )
        self.unparsed_characters.append(numeric_character)

    def scanSubtraction(self, index: int):
        if len(self.parsed_tokens) == 0 and len(self.unparsed_characters) == 0:
            self.unparsed_characters.append("-")
            return

        if len(self.unparsed_characters) > 0:
            if self.unparsed_characters[-1] == "-":
                raise Exception(
                    f"- sign cannot be placed after {self.unparsed_characters[-1]} sign at index {index}"
                )
            else:
                self.parseUnparsedCharacters()
                self.parsed_tokens.append(Token("sign", "-"))
                return

        if len(self.parsed_tokens) > 0:
            if self.parsed_tokens[-1].value in ("-", "+", "*", "/"):
                raise Exception(
                    f"- sign cannot be placed after {self.parsed_tokens[-1].value} sign at index {index}"
                )
            if self.parsed_tokens[-1].value == "(":
                self.unparsed_characters.append("-")
                return
            self.parsed_tokens.append(Token("sign", "-"))
            return

    def scanAddition(self, index: int):
        if len(self.unparsed_characters) > 0:
            if self.unparsed_characters[-1] != "-":
                self.parseUnparsedCharacters()
                self.parsed_tokens.append(Token("sign", "+"))
                return
            else:
                raise Exception(
                    f"+ sign cannot be placed after {self.unparsed_characters[-1]} sign at index {index}"
                )

        if len(self.parsed_tokens) > 0:
            if self.parsed_tokens[-1].value in ("(", "+", "-", "*", "/", "="):
                raise Exception(
                    f"+ sign cannot be placed after {self.parsed_tokens[-1].value} sign at index {index}"
                )
            elif self.parsed_tokens[-1].value == ")" or self.parsed_tokens[-1].token_tag == 'variable':
                self.parsed_tokens.append(Token("sign", "+"))
                return

    def scanMultiplication(self, index: int):
        if len(self.unparsed_characters) > 0:
            if self.unparsed_characters[-1] != "-":
                self.parseUnparsedCharacters()
                self.parsed_tokens.append(Token("sign", "*"))
                return
            else:
                raise Exception(
                    f"* sign cannot be placed after {self.unparsed_characters[-1]} sign at index {index}"
                )

        if len(self.parsed_tokens) > 0:
            if self.parsed_tokens[-1].value in ("(", "+", "-", "*", "/", "="):
                raise Exception(
                    f"* sign cannot be placed after {self.parsed_tokens[-1].value} sign at index {index}"
                )
            elif self.parsed_tokens[-1].value == ")" or self.parsed_tokens[-1].token_tag == 'variable':
                self.parsed_tokens.append(Token("sign", "*"))
                return

    def scanDivision(self, index: int):
        if len(self.unparsed_characters) > 0:
            if self.unparsed_characters[-1] != "-":
                self.parseUnparsedCharacters()
                self.parsed_tokens.append(Token("sign", "/"))
                return
            else:
                raise Exception(
                    f"/ sign cannot be placed after {self.parsed_tokens[-1].value} sign at index {index}"
                )

        if len(self.parsed_tokens) > 0:
            if self.parsed_tokens[-1].value in ("(", "+", "-", "*", "/", "="):
                raise Exception(
                    f"/ sign cannot be placed after {self.parsed_tokens[-1].value} sign at index {index}"
                )
            elif self.parsed_tokens[-1].value in ")" or self.parsed_tokens[-1].token_tag == 'variable':
                self.parsed_tokens.append(Token("sign", "/"))
                return

    def scanOpenParenthesis(self, index: int):
        if len(self.unparsed_characters) == 0:
            if len(self.parsed_tokens) > 0:
                if self.parsed_tokens[-1].value not in ("(", "+", "-", "*", "/", ")"):
                    raise Exception(
                        f"( sign cannot be placed after a(n) {self.parsed_tokens[-1].token_tag} at index {index}"
                    )
                elif self.parsed_tokens[-1].value == ")":
                    raise Exception(
                        f"( sign cannot be placed after ')' sign at index {index}"
                    )
            self.parsed_tokens.append(Token("Parenthesis", "("))
            self.parenthesis_ratio += 1
            return
        elif self.unparsed_characters[-1] == "-":
            self.unparsed_characters = []
            self.parsed_tokens.append(Token("sign", "-"))
            self.parsed_tokens.append(Token("Parenthesis", "("))
            self.parenthesis_ratio += 1
            return
        else:
            raise Exception(
                f"( sign cannot be placed after an integer at index {index}"
            )

    def scanCloseParenthesis(self, index: int):
        if len(self.parsed_tokens) == 0:
            raise Exception(
                f") sign cannot be placed at the beginning of an expression at index {index}"
            )

        if self.parsed_tokens[-1].value == "(":
            if len(self.unparsed_characters) == 0:
                raise Exception(
                    f") sign cannot be placed directly after '(' sign without an expression between them at index {index}"
                )

        isClosingPossible = self.parenthesis_ratio > 0
        if isClosingPossible is False:
            raise Exception(
                f"cannot close a parenthesis that has not been started at index {index}"
            )
        else:
            if len(self.unparsed_characters) > 0:
                if self.unparsed_characters[-1] == "-":
                    raise Exception(
                        f"')' sign cannot be placed after {self.unparsed_characters[-1]} sign at index {index}"
                    )
                else:
                    self.parseUnparsedCharacters()
                    self.parsed_tokens.append(Token("Parenthesis", ")"))
                    self.parenthesis_ratio -= 1
                    return
            else:
                if self.parsed_tokens[-1].value != ")" and self.parsed_tokens[-1].token_tag != 'variable':
                    raise Exception(
                        f"')' sign cannot be placed after {self.parsed_tokens[-1].value} sign at index {index}"
                    )
                else:
                    self.parsed_tokens.append(Token("Parenthesis", ")"))
                    self.parenthesis_ratio -= 1
                    return

    def scanVariable(self, variable: str, index: int):
        # assume that variable is single character
        if len(self.unparsed_characters) > 0:
            if self.unparsed_characters[-1] == '-':
                self.unparsed_characters.clear()
                self.parsed_tokens.append(Token("sign", '-'))
                self.parsed_tokens.append(Token("variable", variable))
            else:
                raise Exception(f"Cannot place a variable after a number at index {index}")
            return
        if len(self.parsed_tokens) > 0:
            if self.parsed_tokens[-1].value == ")":
                raise Exception(
                    f"Cannot place a variable after a closed parenthesis at index {index}"
                )
            if self.parsed_tokens[-1].token_tag == 'variable':
                raise Exception(
                    f"Cannot place a variable after another variable at index {index}"
                )
            self.parsed_tokens.append(Token("variable", variable))
            return
        else:
            self.parsed_tokens.append(Token("variable", variable))

    def scanEquals(self, index: int):
        if len(self.parsed_tokens) == 0 and len(self.unparsed_characters) == 0:
            raise Exception(
                f"Cannot place a equals sign at the beginning at index {index}"
            )
        if self.parenthesis_ratio:
            raise Exception(
                f"Opened parenthesis have not been closed at index {index}!"
            )
        if self.unparsed_characters:
            if self.unparsed_characters[-1] == '-':
                raise Exception(
                    f"Cannot place a equals sign after '-' sign at index {index}"
                )
            else:
                self.parseUnparsedCharacters()
                self.parsed_tokens.append(Token('equals sign', '='))
                return
        if self.parsed_tokens:
            if self.parsed_tokens[-1].token_tag == 'sign':
                raise Exception(
                    f"Cannot place a equals sign after {self.parsed_tokens[-1].value} sign at index {index}"
                )

        self.parsed_tokens.append(Token('equals sign', '='))


    def parseUnparsedCharacters(self):
        string_number = "".join(self.unparsed_characters)
        self.parsed_tokens.append(Token("integer", string_number))
        self.unparsed_characters = []

    def printTokens(self):
        for token in self.parsed_tokens:
            print(token.token_tag, " ", token.value)
