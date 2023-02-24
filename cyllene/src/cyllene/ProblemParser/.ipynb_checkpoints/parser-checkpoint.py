"""Problem File Parser

This module allows the user to convert a string in Problem format into a dictionary format. 

It may also be used to parse singular Problem sections.

This file can also be imported as a module and contains the following
functions:
    * parse - parses a .prob file, returns dictionary
    * parse_section - parsing subroutine for each section
    * prepText - prepares raw text for insertion into Markdown
    * parse_as_list - separates raw list into parsed list
    * parse_as_value - interprets Python value from raw
"""

import re
from pyparsing import *
from numpy import NAN
from ast import literal_eval

from re import VERBOSE
number = Regex(r"""
        [+-]?                           # optional sign
         (
            (?:\d+(?P<float1>\.\d*)?)   # match 2 or 2.02
          |                             # or
            (?P<float2>\.\d+)           # match .02
         )
         (?P<float3>[Ee][+-]?\d+)?      # optional exponent
        """, flags=VERBOSE
               )


def convertNumber(t):
    """Convert a string matching a number to a python number"""
    if t.float1 or t.float2 or t.float3:
        return [float(t[0])]
    else:
        return [int(t[0])]


number.setParseAction(convertNumber)

# dealing with raw text
# anything after the '#' character is considered as a comment and skipped
# a raw value can be on several lines, but
#   any additional lines must start with whitespace and not with [
rawLine = CharsNotIn('#\n') + (lineEnd | Suppress('#'+restOfLine))
rawValue = Combine(
    rawLine + ZeroOrMore(White(' \t').suppress() + NotAny('[') + rawLine))
rawValue.setParseAction(lambda t: [x.strip() for x in t])

# Keyword: detect fixed Python values to replace them appropriately
# QuotedString: detect quoted string and unquote
# MatchFirst: build super element for all kinds of Python values
pyValue_list = [number,
                Keyword('True').setParseAction(replaceWith(True)),
                Keyword('False').setParseAction(replaceWith(False)),
                Keyword('NAN', caseless=True).setParseAction(replaceWith(NAN)),
                QuotedString('"""', multiline=True),
                QuotedString("'''", multiline=True),
                QuotedString('"'),
                QuotedString("'")]
# parse valid Python value
pyValue = MatchFirst(e.setWhitespaceChars(' \t\r') for e in pyValue_list)
# parse simple array of pyValues
arrayValue = Suppress("[") + Optional(ZeroOrMore(pyValue +
                                                 Suppress(","))) + Optional(pyValue) + Suppress("]")
# parse valid Python key name
keyName = Word(alphas+"_", alphanums+"_")
# parse value, either a Python value or raw
valueDef = pyValue | rawValue
# parse key-value pair
tag_pattern = keyName('key') + Suppress(":"+empty) + valueDef('value')
# parse start of a new section
section_pattern = Suppress("<<") + Word(alphas) + Suppress(">>")
# parse zeroth element of a list
zerothPattern = Suppress('-') + restOfLine


def prepText(text: str) -> str:
    """Return a manicured version of the text suitable for Markdown display"""
    # convert '\bf{}' to '<b> </b>'
    pattern = re.compile(r"\\bf\{(.*?)\}")
    text = pattern.sub(r"<b>\1</b>", text)

    # convert '\it{}' to '<i> </i>'
    pattern = re.compile(r"\\it\{(.*?)\}")
    text = pattern.sub(r"<i>\1</i>", text)

    # convert '\uline{}' to '<i> </i>'
    pattern = re.compile(r"\\uline\{(.*?)\}")
    text = pattern.sub(r"<i>\1</i>", text)

    # convert display math brackets '\[ \]' to '$'
    pattern = re.compile(r"\\\[\s*(.*?)\s*\\\]")
    text = pattern.sub(r"$\1$", text)

    # convert '<center> </center>' to text-aligns
    pattern = re.compile(r"<center>(.*?)</center>")
    text = pattern.sub(r'<p style="text-align:center">\1</p>', text)

    return text


def parse_as_list(string: str) -> list:
    """Parse an itemized list of basic Python values. Return delimited list"""
    delimited = string.split(sep='\n-')
    delimited = [d.strip() for d in delimited]
    # remove the first item's '-'
    delimited[0] = zerothPattern.parseString(delimited[0])[0].strip()
    return delimited


def parse_as_value(string: str):
    """Parse string representing Python value either as array or non-array"""
    try:
        # value is an array
        p = arrayValue.parseString(string)
        return [v for v in p]
    except:
        # value is not an array
        return string


def parse_section(section, contents):
    section = section.lower()
    parsed_lines = ""

    # parse through lines of contents in an appropriate way
    for line in contents.splitlines():
        if not line == "":
            # remember the original line breaks for these sections
            if(section in ["parameters", "choices", "info"]):
                parsed_lines = parsed_lines + line.rstrip() + '\n'
            # forget the original line breaks for remaining sections
            else:
                parsed_lines = parsed_lines + line.strip()

    if(section in ['parameters', 'info']):
        try:
            return literal_eval("{" + parsed_lines + "}")
        except:
            return {}
    if(section in ['statement', 'solution', 'answer']):
        try:
            return prepText(parsed_lines)
        except:
            return ""
    if(section == 'choices'):
        try:
            return parse_as_list(parsed_lines)
        except:
            return [""]


def parse(instring: str) -> dict:
    """Parse string in Problem format 

    This script converts a string in Problem format to its corresponding dictionary format.

    This script requires that `pyparsing` be installed within the Python
    environment in which you are running this script.

    :param instring: string to be parsed
    :returns: a dictionary with the problem components
    """
    return_dict = {}

    # split string into lines
    lines = instring.splitlines()
    currentSection = None

    # parse non-empty lines one by one
    for line in lines:
        if line:
            # remove in-line comments
            line = line.partition('#')[0]
            try:
                # starting a new section
                currentSection = section_pattern.parseString(line.strip())[
                    0].lower()
                return_dict[currentSection] = ""
            except:
                # continuing to add to current section
                if currentSection:
                    return_dict[currentSection] = return_dict[currentSection] + '\n' + line

    # parse each section individually
    for key in return_dict.keys():
        return_dict[key] = parse_section(key, return_dict[key])

    # return_dict['parameters'] = parse_section(
    #     'parameters', return_dict['parameters'])
    # return_dict['statement'] = parse_section(
    #     'statement', return_dict['question'])
    # return_dict['answer'] = parse_section('answer', return_dict['answer'])
    # return_dict['choices'] = parse_section('choices', return_dict['choices'])
    # return_dict['solution'] = parse_section(
    #     'solution', return_dict['solution'])
    # info = parse_section('info', return_dict['info'])

    # # copy 'question' to 'statement'
    # return_dict['statement'] = return_dict['question']

    # unpack info into overall dictionary
    if 'info' in return_dict.keys():
        for key, value in return_dict['info'].items():
            return_dict[key] = value

    # rename key "id" to "problem_id"
    if 'id' in return_dict.keys():
        return_dict['problem_id'] = return_dict['id']

    # remove any unnecessary keys
    remnant_keys = ['info', 'id']
    for key in remnant_keys:
        try:
            del return_dict[key]
        except:
            pass

    return return_dict
