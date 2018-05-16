# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

from .topping import Topping
import sys

try:
    from pygments import highlight
    from pygments.lexers import JavaLexer
    from pygments.formatters import HtmlFormatter
    SYNTAX_HIGHLIGHT = True
    FORMATTER = HtmlFormatter(classprefix="hl_", nowrap=True)
    LEXER = JavaLexer()
except:
    import traceback
    import sys
    print("Failed to load syntax highlighter; is pygments installed?  Code will not be highlighted.", file=sys.stderr)
    traceback.print_exc()
    SYNTAX_HIGHLIGHT = False


class PacketsTopping(Topping):
    KEY = "packets.packet"
    NAME = "Packets"
    ITEMS = ("Direction",
             ("id", "ID"),
             ("size", "Size"),
             ("code", None))
    SORTING = Topping.NUMERIC_SORT
    NO_ESCAPE = ("code")
    ESCAPE_TITLE = False

    DIRECTIONS = {(True, True): "Both",
                  (True, False): "Client to server",
                  (False, True): "Server to client",
                  (False, False): "None"}
    TYPES = {"byte": "writeByte",
             "boolean": "writeBoolean",
             "short": "writeShort",
             "int": "writeInt",
             "float": "writeFloat",
             "long": "writeLong",
             "double": "writeDouble",
             "string": "writeString",
             "byte[]": "writeBytes",
             "varint": "writeVarInt",
             "varlong": "writeVarLong",
             "metadata": "writeMetadata",
             "position": "writePosition",
             "uuid": "writeUUID",
             "enum": "writeVarIntEnum",
             "nbtcompound": "writeNBTCompound",
             "itemstack": "writeItemStack",
             "chatcomponent": "writeChatComponent",
             "varint[]": "writeVarIntArray",
             "long[]": "writeLongArray",
             "identifier": "writeIdentifier"
        }
    PRIORITY = 7

    def parse_entry(self, entry, key):
        entry["Direction"] = self.DIRECTIONS[(
            entry["from_client"],
            entry["from_server"]
        )]
        if "instructions" in entry:
            entry["code"] = self.code(entry["instructions"])
        else:
            entry["code"] = ""

        title = key
        if "name" in entry:
            title = "%s (%s)" % (entry["name"], title)
        elif self.wiki_links:
            title = "%s (%s)" % (self.wiki.name(entry["id"], "Unknown"), title)

        return (title, key)

    def links(self, entry, key=None):
        if self.wiki_links and self.wiki.url(entry["id"]) is not None:
            yield ("wiki", self.wiki.url(entry["id"]))

    def code(self, instructions):
        code = self.instructions(instructions)
        if SYNTAX_HIGHLIGHT:
            code = highlight(code, LEXER, FORMATTER)
        else:
            code = self.escape(code)
        return "<pre>%s</pre>" % code

    def instructions(self, instructions, level=0):
        close = False
        case = False
        aggregate = ""
        if instructions:
            for instr in instructions:
                html, close, case = self.instruction(instr, close, case, level)
                aggregate += html
        else:
            aggregate += self.indent("// empty", level);
        if close:
            aggregate += self.indent("}", level)
        return aggregate

    def instruction(self, instr, close=False, case=False, level=0):
        aggregate = ""
        if case:
            level += 1
        if close:
            aggregate = self.indent("}", level)
        close = True
        if instr["operation"] == "write":
            aggregate += self.indent("%s(%s);" % (
                self.TYPES[instr["type"]],
                instr["field"]
            ), level)
            close = False
        elif instr["operation"] == "if":
            aggregate += self.indent("if(%s) {" % instr["condition"], level)
            aggregate += self.instructions(instr["instructions"], level + 1)
        elif instr["operation"] == "else":
            aggregate = self.indent("} else {", level)
            aggregate += self.instructions(instr["instructions"], level + 1)
        elif instr["operation"] == "loop":
            aggregate += self.indent("while(%s) {" % instr["condition"], level)
            aggregate += self.instructions(instr["instructions"], level + 1)
        elif instr["operation"] == "switch":
            aggregate += self.indent("switch(%s) {" % instr["field"], level)
            aggregate += self.instructions(instr["instructions"], level + 1)
        elif instr["operation"] == "case":
            if case:
                level -= 1
            aggregate += self.indent("case %s:" % instr["value"], level)
            close = False
            case = True
        elif instr["operation"] == "break":
            aggregate += self.indent("break;", level)
            close = False
        elif instr["operation"] == "increment":
            if instr["amount"] == "1":
                aggregate += self.indent("%s++;" % instr["field"], level)
            else:
                aggregate += self.indent("%s += %s;" % (
                    instr["field"],
                    instr["amount"]
                ), level)
            close = False
        elif instr["operation"] == "store":
            aggregate += self.indent("%s %s = %s;" % (
                instr["type"],
                instr["var"],
                instr["value"]
            ), level)
            close = False
        elif instr["operation"] == "arraystore":
            aggregate += self.indent("%s[%s] = %s;" % (
                instr["var"],
                instr["index"],
                instr["value"]
            ), level)
            close = False
        elif instr["operation"] == "interfacecall":
            aggregate += self.indent(
            "%s.%s(%s); // %s call to %s.%s: behavior may vary" % (
                instr["field"],
                instr["name"],
                instr["args"],
                instr["type"],
                instr["target"],
                instr["method"]
            ), level)
            close = False
        else:
            aggregate += self.indent("// %s" % instr["operation"], level)
            close = False
        return (aggregate, close, case)

    def indent(self, string, level):
        return "  " * level + string + "\n"
