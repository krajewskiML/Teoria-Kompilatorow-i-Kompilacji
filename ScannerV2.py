from collections import namedtuple
from typing import List, Tuple

Token = namedtuple("Token", ["token_tag", "value"])
SIGNS = ["+", "-", "*", "/", "=", "<", ">"]
COMMAS = [";", ","]
PARENTHESIS = ["(", ")", "{", "}"]
KEYWORDS = ["for", "if", "else", "return", "def", "switch", "case", "do", "while"]
TYPES = ["int", "float", "double", "long", "bool", "void"]


class IdxYieldingScanner:
    def __init__(self):
        self.parsed_lines = []

    def scan_file(self, path_to_file: str) -> None:
        with open(path_to_file, "r") as fin:
            lines = [[char for char in line] for line in fin]

        for line_idx, line in enumerate(lines):
            scanned_line = self._scan_line(line, line_idx)
            if scanned_line:
                self.parsed_lines.append(scanned_line)

    def _scan_line(self, chars: List[str], line: int) -> List[Token]:
        char_count = len(chars)
        index = 0
        scanned_tokens = []
        while index < char_count:
            if chars[index] == "#":
                return scanned_tokens
            if chars[index].isspace():
                index = index + 1
                continue
            if chars[index].isnumeric():
                index, token = self.scanNumeric(index, chars, line)
            elif chars[index].isalpha():
                index, token = self.scanAlphabetic(index, chars, line)
            elif chars[index] in SIGNS:
                index, token = index + 1, Token("sign", chars[index])
            elif chars[index] in PARENTHESIS:
                index, token = index + 1, Token("parenthesis", chars[index])
            elif chars[index] in COMMAS:
                index, token = index + 1, Token("comma", chars[index])
            else:
                raise Exception(
                    f"unknown character: {chars[index]} at {index} in line {line + 1}"
                )

            scanned_tokens.append(token)

        return scanned_tokens

    def scanNumeric(self, index: int, chars: List[str], line: int) -> Tuple[int, Token]:
        iterator = index
        digits = ""
        while iterator < len(chars) and (
            chars[iterator].isnumeric()
            or chars[iterator].isalpha()
            or chars[iterator] == "."
        ):
            if chars[iterator].isalpha():
                raise Exception(
                    f"number can not contain a letter at index {iterator} in line {line + 1}"
                )
            digits += chars[iterator]
            iterator += 1

        if digits.count(".") == 0:
            return iterator, Token("integer", int(digits))
        if digits.count(".") == 1:
            return iterator, Token("float", float(digits))
        else:
            raise Exception(
                f"numeric value can be build using only 1 dot, in line {line + 1}"
            )

    def scanAlphabetic(
        self, index: int, chars: List[str], line: int
    ) -> Tuple[int, Token]:
        iterator = index
        letters = ""
        while iterator < len(chars) and (
            chars[iterator].isalpha() or chars[iterator].isnumeric()
        ):
            letters += chars[iterator]
            iterator += 1

        if letters in KEYWORDS:
            return iterator, Token("keyword", letters)
        if letters in TYPES:
            return iterator, Token("data_type", letters)
        else:
            return iterator, Token("variable", letters)

    def printTokens(self):
        for line in self.parsed_lines:
            for token in line:
                print(token.token_tag, " ", token.value, end=", ")
            print()

    def colourTokens(self, out_path: str):
        with open(out_path, "w") as fout:
            fout.write("<body bgcolor='#2b2b2b'>")
            for line in self.parsed_lines:
                fout.write("<br>")
                for parsed_token in line:
                    if parsed_token.token_tag == "variable":
                        fout.write(
                            '<span style="color:#ffffff">%s </span>'
                            % parsed_token.value
                        )
                    if parsed_token.token_tag in ["sign", "parenthesis"]:
                        fout.write(
                            '<span style="color:#ff0000">%s </span>'
                            % parsed_token.value
                        )
                    if parsed_token.token_tag == "data_type":
                        fout.write(
                            '<span style="color:#b200b2">%s </span>'
                            % parsed_token.value
                        )
                    if parsed_token.token_tag in ["integer", "float"]:
                        fout.write(
                            '<span style="color:#6897bb">%s </span>'
                            % parsed_token.value
                        )
                    if parsed_token.token_tag in ["comma", "keyword"]:
                        fout.write(
                            '<span style="color:#cc7832">%s </span>'
                            % parsed_token.value
                        )
                fout.write("</br>")
            fout.write("</body>")
