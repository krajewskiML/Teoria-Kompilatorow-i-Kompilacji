from collections import namedtuple
from typing import List

Token = namedtuple("Token", ["kod", "wartosc"])


class Scanner:
    def __init__(self):
        self.parsed_tokens: List[Token] = []
        self.unparsed_characters: List[str] = []

    def scan_file(self, path: str):
        with open(path, "r") as fin:
            characters = [
                character for character in next(fin) if not character.isspace()
            ]

        for idx, character in enumerate(characters):
            self.scan(character)

        if len(self.unparsed_characters) > 0:
            if self.unparsed_characters[-1] == "-":
                raise Exception("asiodjf")
            else:
                self.parseUnparsedCharacters()

        # not enough closing parenthesis
        availableClosing = 0
        for token in self.parsed_tokens:
            if token.wartosc == "(":
                availableClosing += 1
            if token.wartosc == ")":
                availableClosing -= 1

        if availableClosing > 0:
            raise Exception("szmra")

        # last char is sign
        if self.parsed_tokens[-1].wartosc in ("-", "+", "*", "/"):
            raise Exception("og olgierd")

    def scan(self, character: str):
        if character.isnumeric():
            self.scanNumeric(character)
        if character == "-":
            self.scanSubtraction()
        if character == "+":
            self.scanAddition()
        if character == "*":
            self.scanMultiplication()
        if character == "/":
            self.scanDivision()
        if character == "(":
            self.scanOpenParenthesis()
        if character == ")":
            self.scanCloseParenthesis()

    def scanNumeric(self, numeric_character: str):
        if len(self.parsed_tokens) > 0 and self.parsed_tokens[-1].wartosc == ")":
            raise Exception("iashdfiuh")
        self.unparsed_characters.append(numeric_character)

    def scanSubtraction(self):
        if len(self.parsed_tokens) == 0 and len(self.unparsed_characters) == 0:
            self.unparsed_characters.append("-")
            return

        if len(self.unparsed_characters) > 0:
            if self.unparsed_characters[-1] in ("-", "+", "*", "/"):
                raise Exception("sraka")
            else:
                self.parseUnparsedCharacters()
                self.parsed_tokens.append(Token("sign", "-"))
                return

        if len(self.parsed_tokens) > 0:
            if self.parsed_tokens[-1].wartosc in ("-", "+", "*", "/"):
                raise Exception("sraka")
            if self.parsed_tokens[-1].wartosc == "(":
                self.unparsed_characters.append("-")
                return
            self.parsed_tokens.append(Token("sign", "-"))
            return

        raise Exception("sraka")

    def scanAddition(self):
        if len(self.unparsed_characters) > 0:
            if self.unparsed_characters[-1] != "-":
                self.parseUnparsedCharacters()
                self.parsed_tokens.append(Token("sign", "+"))
                return

        if len(self.parsed_tokens) > 0:
            if self.parsed_tokens[-1].wartosc in ("(", "+", "-", "*", "/"):
                raise Exception("sra")
            elif self.parsed_tokens[-1].wartosc == ")":
                self.parsed_tokens.append(Token("sign", "+"))
                return

        raise Exception("gowno1")

    def scanMultiplication(self):
        if len(self.unparsed_characters) > 0:
            if self.unparsed_characters[-1] != "-":
                self.parseUnparsedCharacters()
                self.parsed_tokens.append(Token("sign", "*"))
                return

        if len(self.parsed_tokens) > 0:
            if self.parsed_tokens[-1].wartosc in ("(", "+", "-", "*", "/"):
                raise Exception("sra")
            elif self.parsed_tokens[-1].wartosc == ")":
                self.parsed_tokens.append(Token("sign", "*"))
                return

        raise Exception("gowno1")

    def scanDivision(self):
        if len(self.unparsed_characters) > 0:
            if self.unparsed_characters[-1] != "-":
                self.parseUnparsedCharacters()
                self.parsed_tokens.append(Token("sign", "/"))
                return

        if len(self.parsed_tokens) > 0:
            if self.parsed_tokens[-1].wartosc in ("(", "+", "-", "*", "/"):
                raise Exception("sra")
            elif self.parsed_tokens[-1] == ")":
                self.parsed_tokens.append(Token("sign", "/"))
                return

        raise Exception("gowno1")

    def scanOpenParenthesis(self):
        if len(self.unparsed_characters) == 0:
            if len(self.parsed_tokens) > 0:
                if self.parsed_tokens[-1].wartosc not in ("(", "+", "-", "*", "/"):
                    raise Exception("elo")
            self.parsed_tokens.append(Token("sign", "("))
            return
        elif self.unparsed_characters[-1] == "-":
            self.unparsed_characters = []
            self.parsed_tokens.append(Token("sign", "-"))
            self.parsed_tokens.append(Token("sign", "("))
            return

        raise Exception("elo")

    def scanCloseParenthesis(self):
        if len(self.parsed_tokens) == 0:
            raise Exception("motyla noga")

        if self.parsed_tokens[-1].wartosc == "(":
            if len(self.unparsed_characters) == 0:
                raise Exception("cholipka")

        availableClosing = 0
        for token in self.parsed_tokens:
            if token.wartosc == "(":
                availableClosing += 1
            if token.wartosc == ")":
                availableClosing -= 1

        isClosingPossible = availableClosing > 0
        if isClosingPossible is False:
            raise Exception("skra")
        else:
            if len(self.unparsed_characters) > 0:
                if self.unparsed_characters[-1] == "-":
                    raise Exception("szmraaa")
                else:
                    self.parseUnparsedCharacters()
                    self.parsed_tokens.append(Token("sign", ")"))
                    return
            else:
                if self.parsed_tokens[-1].wartosc != ")":
                    raise Exception("nota number")
                else:
                    self.parsed_tokens.append(Token("sign", ")"))
                    return

    def parseUnparsedCharacters(self):
        string_number = "".join(self.unparsed_characters)
        self.parsed_tokens.append(Token("integer", string_number))
        self.unparsed_characters = []
