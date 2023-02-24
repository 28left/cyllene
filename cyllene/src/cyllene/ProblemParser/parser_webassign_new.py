"""WebAssign Problem Parser

This module allows the user to convert a string in WebAssign (.wa) 
or Python Webassign (.pwa) formats into a dictionary format.

This file can also be imported as a module and contains the following
functions:
    * parse_webassign - parses a .wa/.pwa file, returns dictionary
    * parse_section - parsing subroutine for each section
    * remove_dollars - removes Pearl susbsitution identifiers
    * clean_text - tailor syntax of string to fit Markdown.
"""

import re
from pyparsing import *
from ast import literal_eval
from copy import deepcopy

# format of contents of each section from WebAssign file
question_pattern = CaselessLiteral("<eqn>").suppress() + ... + CaselessLiteral("''</eqn>").suppress() + Suppress(
    Optional(White())) + Suppress("<watex>") + ... + Suppress("</watex>") + Suppress(Optional(White())) + Suppress("<_>")
answer_pattern = Suppress("<watex>") + ... + Suppress("</watex>")
solution_pattern = Suppress("<watex>") + ... + Suppress("</watex>")

# possible sections to parse
info_section_pattern = Literal("Info")
question_section_pattern = Literal("Question")
answer_section_pattern = Literal("Answer")
solution_section_pattern = Literal("Solution")

# a section comes of one of the above four forms
section_pattern = info_section_pattern ^ question_section_pattern ^ answer_section_pattern ^ solution_section_pattern


def remove_dollars(string: str) -> str:
    """
    Remove wrapping ${...} or prefix $... from string
    """
    # first catch '${...}'
    pattern = re.compile(r"\$\{(\w+)(\[)?\$?(\w+\])?\}")
    string = pattern.sub(r"\1\2\3", string)

    # now simple '$...'
    pattern = re.compile(r"\$(\w+)(\[)?\$?(\w+\])?")
    string = pattern.sub(r"\1\2\3", string)

    return string


def clean_text(string: str) -> str:
    """
    Return a manicured version of the text suitable 
    for Markdown display
    """
    string = string.strip()

    # convert '<eqn ...>' to '@{...}'
    #   1. Identify all of the places where <eqn ...> occurs
    eqn_tag_list = re.findall(r"<(?:eqn|EQN) .*?>", string)

    # for eqn in eqn_tag_list:
    #     print(eqn)

    #   2. Remove any dollars occurring in this tag
    dollarless_tag_list = [remove_dollars(tag) for tag in eqn_tag_list]
    #   3. Replace in the original string
    for index, tag in enumerate(eqn_tag_list):
        string = string.replace(tag, dollarless_tag_list[index])
    #   4. Now change each <eqn ...> to @{...}
    pattern = re.compile(r"<(eqn|EQN) (.*?)>")
    string = pattern.sub(r"@{\2}", string)

    # convert '<eqn> ... </eqn>' to '@{...}' (not multi-line)
    #   1. Identify all of the places where <eqn ...> occurs
    eqn_tag_list = re.findall(r"<(?:eqn|EQN)>.*?</(?:eqn|EQN)>", string)
    #   2. Remove any dollars occurring in this tag
    dollarless_tag_list = [remove_dollars(s) for s in eqn_tag_list]
    #   3. Replace in the original string
    for index, tag in enumerate(eqn_tag_list):
        string = string.replace(tag, dollarless_tag_list[index])
    #   4. Now change each <eqn> ... </eqn> to @{...}
    pattern = re.compile(r"<(eqn|EQN)>(.*?)</(eqn|EQN)>")
    string = pattern.sub(r"@{\2}", string)

    # convert '${...}' to '@{...}'
    pattern = re.compile(r"\$\{(\w+)(\[)?\$?(\w+\])?\}")
    string = pattern.sub(r"@{\1\2\3}", string)

    # convert '$...' to '@{...}'
    pattern = re.compile(r"\$(\w+)(\[)?\$?(\w+\])?")
    string = pattern.sub(r"@{\1\2\3}", string)

    # convert watex specific notation
    string = string.replace("<s:union>", "\\cup")
    string = string.replace("<s:intersect>", "\\cap")
    string = string.replace("<s:element>", "\\in")

    # convert '\bf{...}' to '<b>...</b>'
    pattern = re.compile(r"\\bf\{(.*?)\}")
    string = pattern.sub(r"<b>\1</b>", string)

    # convert '\it{...}' to '<i>...</i>'
    pattern = re.compile(r"\\it\{(.*?)\}")
    string = pattern.sub(r"<i>\1</i>", string)

    # convert '\uline{...}' to '<i>...</i>'
    pattern = re.compile(r"\\uline\{(.*?)\}")
    string = pattern.sub(r"<i>\1</i>", string)

    # convert display math brackets '\[...\]' to '$...$'
    pattern = re.compile(r"\\\[\s*(.*?)\s*\\\]")
    string = pattern.sub(r"$\1$", string)

    # convert '<center> </center>' to text-aligns
    pattern = re.compile(r"<center>(.*?)</center>")
    string = pattern.sub(r'<p style="text-align:center">\1</p>', string)

    return string


def parse_answer(answer_line):
    """
    Parse a line found in the answers section in one of two ways
    """
    try:
        return answer_pattern.parseString(answer_line)[0]
    except:
        return answer_line


def parse_section(section: str, contents: str):
    """
    Parse a string identified by its section.
    """
    section = section.lower()

    if (section == 'info'):
        try:
            return literal_eval("{" + contents + "}")
        except:
            return {}
    if (section in ['statement', 'solution', 'answer']):
        try:
            return clean_text(contents)
        except:
            return ""
    if (section == 'choices'):
        try:
            return [clean_text(parse_answer(line)) for line in contents.splitlines()]
        except:
            return ['']


def parse_webassign(instring: str) -> dict:
    """Parse string in a WebAssign format.

    This script converts a string in the WebAssign format to its corresponding dictionary format.

    This script requires that `pyparsing` be installed.

    :param instring: string to be parsed
    :returns: a dictionary with the problem components
    """
    return_dict = {}

    # split string into lines
    lines = instring.splitlines()
    currentSection = None

    # parse non-empty lines one-by-one
    for line in lines:
        # remove in-line comments
        line = line.partition('#')[0]
        if line:
            # decide if we can start a new section
            try:
                currentSection = section_pattern.parseString(line.strip())[
                    0].lower()
                return_dict[currentSection] = ""
            # otherwise, continue to add to current section
            except:
                if currentSection:
                    # remove line breaks in these sections
                    if currentSection in ['solution']:
                        # if currentSection in ['question', 'solution']:
                        return_dict[currentSection] = return_dict[currentSection] + line
                    # preserve line breaks in these sections
                    # in Question they need to be preserved to execute code part properly
                    else:
                        return_dict[currentSection] = return_dict[currentSection] + line + '\n'

    # perform case work due to the WebAssign syntax
    for key in deepcopy(return_dict).keys():
        if key == 'question':
            code_contents, statement_contents = question_pattern.parseString(
                return_dict[key])
            return_dict['parameters'] = {
                'code': code_contents
            }
            return_dict['statement'] = parse_section(
                'statement', statement_contents)
        if key == 'answer':
            return_dict['choices'] = parse_section(
                'choices', return_dict['answer'])
        if key == 'solution':
            return_dict['solution'] = parse_section(
                'solution', solution_pattern.parseString(return_dict['solution'])[0])
        if key == 'info':
            return_dict['info'] = parse_section(key, return_dict['info'])

    # unpack info into overall dictionary
    if 'info' in return_dict.keys():
        for key, value in return_dict['info'].items():
            return_dict[key] = value

    # rename key "id" to "problem_id"
    if 'id' in return_dict.keys():
        return_dict['problem_id'] = return_dict['id']

    # remove any unnecessary keys
    remnant_keys = ['info', 'id', 'question', 'answer']
    for key in remnant_keys:
        try:
            del return_dict[key]
        except:
            pass

    return return_dict
