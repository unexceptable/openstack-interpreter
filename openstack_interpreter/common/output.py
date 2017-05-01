
from fcntl import ioctl
import os
import textwrap
import struct
import sys
import termios
import json
import prettytable


# wrap has to be a parameter to allow these to be used as formatters.
def red(text, wrap=None):
    if sys.stdout.isatty() and not os.getenv('ANSI_COLORS_DISABLED'):
        text = '\033[31m%s\033[0m' % text
    return text


def print_red(text):
    print(red(text))


def yellow(text, wrap=None):
    if sys.stdout.isatty() and not os.getenv('ANSI_COLORS_DISABLED'):
        text = '\033[33m%s\033[0m' % text
    return text


def print_yellow(text):
    print(yellow(text))


def green(text, wrap=None):
    if sys.stdout.isatty() and not os.getenv('ANSI_COLORS_DISABLED'):
        text = '\033[32m%s\033[0m' % text
    return text


def print_green(text):
    print(green(text))


def json_formatter(js, wrap=None):
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


def text_wrap_formatter(d, wrap=None):
    return '\n'.join(textwrap.wrap(d or '', wrap or 55))


def newline_list_formatter(r, wrap=None):
    return '\n'.join(r or [])


def print_dict(d, formatters=None, wrap=None, titles=['Property', 'Value'],
               sortby='Property'):
    if not wrap:
        # 2 columns padded by 1 on each side = 4
        # 3 x '|' as border and separator = 3
        # total non-content padding = 7
        padding = 7
        # Now we need to find what the longest key is
        longest_key = 0
        for key in d.keys():
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

    for field in d.keys():
        if field in formatters:
            value = formatters[field](d[field], wrap=wrap)
            pt.add_row([field, value])
        else:
            value = textwrap.fill(str(d[field]), wrap)
            pt.add_row([field, value])
    if sortby:
        print(pt.get_string(sortby=sortby))
    else:
        print(pt.get_string())


def print_list(objs, fields, formatters=None, sortby_index=None,
               mixed_case_fields=None, field_labels=None):
    """Print a list or objects as a table, one row per object.

    :param objs: iterable of :class:`Resource`
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
            if field in formatters:
                row.append(formatters[field](o))
            else:
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


SKULL = """
         ,,_,.-------.,_
     ,;~'             '~;,
   ,;                     ;,
  ;                         ;
 ,'                         ',
,;                           ;,
; ;      .           .      ; ;
| ;   ______       ______   ; |
|  `~"      ~" . "~      "~'  |
|  ~  ,-~~~^~, | ,~^~~~-,  ~  |
 |   |        }:{        |   |
 |   l       / | \       !   |
 .~  (__,.--" .^. "--.,__)  ~.
 |     ---;' / | \ `;---     |
  \__.       \/^\/       .__/
   V| \                 / |V
    | |T~\___!___!___/~T| |
    | |`IIII_I_I_I_IIII'| |
    |  \,III I I I III,/  |
     \   `~~~~~~~~~~'    /
       \   .       .   /
         \.    ^    ./
           ^~~~^~~~^
"""
