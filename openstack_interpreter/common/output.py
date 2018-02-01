"""
This module is all about text formatting and output.

It is suggested you use tab autocomplete to list the available functions
in this class, and inspect them for their docstrings.

E.g.:
In [1]: output.print_styled?
"""

from fcntl import ioctl
import os
import textwrap
import struct
import sys
import termios
import json
import prettytable

available_text_styles = {
    'normal': '0', 'bold': '1', 'faint': '2', 'italic': '3', 'underline': '4',
    'negative': '7', 'strikethrough': '9',

    'black': '30', 'red': '31', 'green': '32', 'yellow': '33', 'blue': '34',
    'magenta': '35', 'cyan': '36', 'white': '37',

    'black-bg': '40', 'red-bg': '41', 'green-bg': '42', 'yellow-bg': '43',
    'blue-bg': '44', 'magenta-bg': '45', 'cyan-bg': '46', 'white-bg': '47',

    'black-bright': '90', 'red-bright': '91', 'green-bright': '92',
    'yellow-bright': '93', 'blue-bright': '94', 'magenta-bright': '95',
    'cyan-bright': '96', 'white-bright': '97',

    'black-bg-bright': '40', 'red-bg-bright': '41', 'green-bg-bright': '42',
    'yellow-bg-bright': '43', 'blue-bg-bright': '44',
    'magenta-bg-bright': '45', 'cyan-bg-bright': '46', 'white-bg-bright': '47',
}


def style_text(text, styles):
    """surround text with ANSI escape codes.

    Depends on support in the terminal you are using.

    :param text: Text to style
    :param styles: list of styles
                   For available style see:
                   In [1]: output.available_text_styles?
    """
    if sys.stdout.isatty() and not os.getenv('ANSI_COLORS_DISABLED'):
        style_codes = []
        for style in styles:
            if style in available_text_styles:
                style_codes.append(available_text_styles[style])
        text = '\033[%sm%s\033[0m' % (";".join(style_codes), text)
    return text


def print_styled(text, styles):
    """print text with ANSI escape codes.

    Depends on support in the terminal you are using.

    :param text: Text to style
    :param styles: list of styles
                   For available style see:
                   In [1]: output.available_text_styles?
    """
    print(style_text(text, styles))


def json_formatter(js, wrap=None):
    """Formatter for json that can wrap it."""
    value = json.dumps(
        js, indent=2, ensure_ascii=False,
        separators=(', ', ': '))
    # as json sort of does it's own line splitting, we have to check
    # if each line is over the wrap limit, and split ourselves.
    if wrap:
        lines = []
        for line in value.split('\n'):
            if len(line) > wrap:
                lines.append(line[0:wrap-1])
                line = line[wrap:]
                while line:
                    lines.append(line[0:wrap-1])
                    line = line[wrap:]
            else:
                lines.append(line)
        value = ""
        for line in lines[:-1]:
            value += "%s\n" % line
        value += "%s" % lines[-1]
    return value


def text_wrap_formatter(text, wrap=None):
    """formatter to wrap the text"""
    return '\n'.join(textwrap.wrap(text or '', wrap or 55))


def newline_list_formatter(text_list, wrap=None):
    """format list with newline for each element"""
    return '\n'.join(text_list or [])


def print_dict(dictionary, formatters=None, wrap=None,
               titles=['Property', 'Value'], sortby=None):
    """
    Will print a prettytable of the given dict.

    :param dictionary: dictionary to print
    :param formatters: `dict` of callables for field formatting
    :param warp: a width value to wrap for.
    :param titles: Labels to use in the heading of the table, default to
        ['Property', 'Value']
    :param sortby: column of the table to sort by, defaults to 'Property'
    .
    """
    if len(titles) != 2:
        print_styled("Titles must exactly 2 values.", ['red'])
    if not sortby:
        sortby = titles[0]
    if not wrap:
        # 2 columns padded by 1 on each side = 4
        # 3 x '|' as border and separator = 3
        # total non-content padding = 7
        padding = 7
        # Now we need to find what the longest key is
        longest_key = 0
        for key in dictionary.keys():
            if len(key) > longest_key:
                longest_key = len(key)
        # the wrap for the value column is based on
        # what is left after we account for the padding
        # and longest key
        wrap = terminal_width() - padding - longest_key

    formatters = formatters or {}
    pt = prettytable.PrettyTable(titles,
                                 caching=False, print_empty=False)
    pt.align = 'l'

    for field in dictionary.keys():
        if field in formatters:
            value = formatters[field](dictionary[field], wrap=wrap)
            pt.add_row([field, value])
        else:
            value = textwrap.fill(str(dictionary[field]), wrap)
            pt.add_row([field, value])
    if sortby:
        print(pt.get_string(sortby=sortby))
    else:
        print(pt.get_string())


def print_object(obj, formatters=None, wrap=None,
                 titles=['Property', 'Value'], sortby='Property'):
    """
    Will print a prettytable of the given object.

    :param obj: object to print
    :param formatters: `dict` of callables for field formatting
    :param warp: a width value to wrap for.
    :param titles: Labels to use in the heading of the table, default to
        ['Property', 'Value']
    :param sortby: column of the table to sort by, defaults to 'Property'
    .
    """

    fields = []
    for field in dir(obj):
        if field.startswith("_") or callable(getattr(obj, field)):
            continue
        fields.append(field)

    if not wrap:
        # 2 columns padded by 1 on each side = 4
        # 3 x '|' as border and separator = 3
        # total non-content padding = 7
        padding = 7
        # Now we need to find what the longest key is
        longest_key = 0
        for key in fields:
            if not key.startswith("_") and len(key) > longest_key:
                longest_key = len(key)
        # the wrap for the value column is based on
        # what is left after we account for the padding
        # and longest key
        wrap = terminal_width() - padding - longest_key

    formatters = formatters or {}
    pt = prettytable.PrettyTable(titles,
                                 caching=False, print_empty=False)
    pt.align = 'l'

    for field in fields:
        if field in formatters:
            value = formatters[field](getattr(obj, field), wrap=wrap)
            pt.add_row([field, value])
        else:
            value = textwrap.fill(str(getattr(obj, field)), wrap)
            pt.add_row([field, value])
    if sortby:
        print(pt.get_string(sortby=sortby))
    else:
        print(pt.get_string())


def print_list(objs, fields, formatters=None, sortby_index=None,
               mixed_case_fields=None, field_labels=None):
    """Print a list or objects as a table, one row per object.

    :param objs: iterable of objects or dicts
    :param fields: attributes that correspond to columns, in order
    :param formatters: `dict` of callables for field formatting
    :param sortby_index: index of the field for sorting table rows
    :param mixed_case_fields: fields corresponding to object attributes that
        have mixed case names (e.g., 'serverId')
    :param field_labels: Labels to use in the heading of the table, default to
        fields.
    """
    formatters = formatters or {}
    mixed_case_fields = mixed_case_fields or []
    field_labels = field_labels or fields
    if len(field_labels) != len(fields):
        raise ValueError(
            "Field labels list %(labels)s has different number "
            "of elements than fields list %(fields)s",
            {'labels': field_labels, 'fields': fields})

    if sortby_index is None:
        kwargs = {}
    else:
        kwargs = {'sortby': field_labels[sortby_index]}
    pt = prettytable.PrettyTable(field_labels)
    pt.align = 'l'

    for o in objs:
        row = []
        for field in fields:
            if field in mixed_case_fields:
                field_name = field.replace(' ', '_')
            else:
                field_name = field.lower().replace(' ', '_')
            data = getattr(o, field_name, '')
            if not data:
                try:
                    data = o.get(field_name, '')
                except Exception:
                    pass
            if field in formatters:
                row.append(formatters[field](data))
            else:
                row.append(data)
        pt.add_row(row)

    print(pt.get_string(**kwargs))


def print_list_rows(rows, headers):
    """
    Print rows using prettytable.
    """
    pt = prettytable.PrettyTable(headers)
    pt.align = 'l'
    for row in rows:
        pt.add_row(row)
    print(pt.get_string())


def terminal_width():
    if hasattr(os, 'get_terminal_size'):
        # python 3.3 onwards has built-in support for getting terminal size
        try:
            return os.get_terminal_size().columns
        except OSError:
            return None
    try:
        # winsize structure has 4 unsigned short fields
        winsize = b'\0' * struct.calcsize('hhhh')
        try:
            winsize = ioctl(sys.stdout, termios.TIOCGWINSZ, winsize)
        except IOError:
            return None
        except TypeError:
            # this is raised in unit tests as stdout is sometimes a StringIO
            return None
        winsize = struct.unpack('hhhh', winsize)
        columns = winsize[1]
        if not columns:
            return None
        return columns
    except IOError:
        return None
