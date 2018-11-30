# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

import sys
import traceback

def usage():
    print("Usage:")
    print("  vitrine_main.py [-b] [-w] [-v] [-r file] [-o file]")
    print()
    print("Options:")
    print("  -b, --body: Don't generate a complete HTML document")
    print("  -w, --wiki: Add links to the MinecraftCoalition wiki and display packet names")
    print("  -v, --verbose: Output progress information to standard error")
    print("  -r, --resources file: Path to resources folder")
    print("  -o, --output file: Output result into a file instead of standard output")
    print("  -h, --help: Show this help")


def import_toppings():
    """
    Attempts to load all available toppings.
    """
    import os

    this_dir = os.path.dirname(__file__)
    toppings_dir = os.path.join(this_dir, "vitrine", "toppings")
    from_list = ["topping"]

    # Traverse the toppings directory and import everything.
    for root, dirs, files in os.walk(toppings_dir):
        for file_ in files:
            if not file_.endswith(".py"):
                continue
            elif file_.startswith("__"):
                continue

            from_list.append(file_[:-3])

    imports = __import__("vitrine.toppings", fromlist=from_list)

    toppings = imports.topping.Topping.__subclasses__()
    subclasses = toppings
    while len(subclasses) > 0:
        newclasses = []
        for subclass in subclasses:
            newclasses += subclass.__subclasses__()
        subclasses = newclasses
        toppings += subclasses

    return toppings


def embed(resources, html):
    return """<!doctype html>
              <html>
                <head>
                  <title>Burger Vitrine</title>
                  <link rel="stylesheet" href="%sstyle.css" />
                  <script src="%sjquery.js"></script>
                  <script src="%svitrine.js"></script>
                </head>
                <body>
                    <div id="vitrine">
                        %s
                    </div>
                </body>
              </html>""" % (resources, resources, resources, html)


def generate_html(toppings, data, all_data=None, wiki=None, highlight=None, progress_callback=None):
    """
    Generates HTML for a version.

    toppings: a list of toppings to run
    data: the data to generate (may be a single-item list, or a dict)
    wiki: Wiki to use for packet names
    highlight: A function taking code that returns HTML
    progress_callback: An optional function to call when starting each
    topping; takes one arg (the topping's name)
    """
    diff = not isinstance(data, list)
    if not diff:
        data = data[0]
    if all_data == None:
        if diff:
            all_data = {False: data, True: data}
        else:
            all_data = data

    # Generate HTML
    aggregate = []

    for topping in sorted(toppings, key=lambda x: -x.PRIORITY):
        if topping.KEY == None:
            continue
        if progress_callback:
            progress_callback(topping.NAME)
        keys = topping.KEY.split(".")
        obj = data
        skip = False
        for key in keys:
            if key not in obj:
                skip = True
                break
            obj = obj[key]
        if skip:
            continue

        try:
            aggregate.append(str(topping(obj, all_data, diff, wiki, highlight)))
        except:
            from html import escape
            aggregate.append('<h2>%s</h2><div class="entry"><h3>Error</h3><pre>%s</pre></div>' % (topping.NAME, escape(traceback.format_exc())))
            print("Failed to run", topping, file=sys.stderr)
            traceback.print_exc()

    return "".join(aggregate)

def main():
    import getopt
    import json
    import functools

    try:
        opts, args = getopt.gnu_getopt(
            sys.argv[1:],
            "o:bwvr:h",
            [
                "output=",
                "body",
                "wiki",
                "verbose",
                "resources=",
                "help",
                "orig_left=",
                "orig_right="
            ]
        )
    except getopt.GetoptError as err:
        print(str(err), file=sys.stderr)
        sys.exit(1)

    # Default options
    output = sys.stdout
    only_body = False
    wiki_links = False
    progress_callback = None
    resources = "resources/"
    all_data = None

    for o, a in opts:
        if o in ("-o", "--output"):
            output = a
        elif o in ("-b", "--body"):
            only_body = True
        elif o in ("-w", "--wiki"):
            wiki_links = True
        elif o in ("-v", "--verbose"):
            progress_callback = functools.partial(print, "Running topping:", file=sys.stderr)
        elif o in ("-r", "--resources"):
            resources = a
            if resources[-1] != "/":
                resources += "/"
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o == "--orig_left":
            if not all_data:
                all_data = {}
            with open(a) as fin:
                data = json.load(fin)
                if isinstance(data, list):
                    data = data[0]
                all_data[False] = data
        elif o == "--orig_right":
            if not all_data:
                all_data = {}
            with open(a) as fin:
                data = json.load(fin)
                if isinstance(data, list):
                    data = data[0]
                all_data[True] = data

    toppings = import_toppings()
    highlight = None

    try:
        import pygments
        from pygments.lexers import JavaLexer
        from pygments.formatters import HtmlFormatter
        formatter = HtmlFormatter(classprefix="hl_", nowrap=True)
        lexer = JavaLexer()
        highlight = lambda code: pygments.highlight(code, lexer, formatter)
    except:
        print("Failed to load syntax highlighter; is pygments installed?  Code will not be highlighted.", file=sys.stderr)
        traceback.print_exc()

    # Load JSON objects from stdin
    if sys.stdin.isatty():
        print("Error: Vitrine expects Burger or Hamburglar output via stdin.\n", file=sys.stderr)
        usage()
        sys.exit(3)

    try:
        data = json.load(sys.stdin)
    except ValueError as err:
        print("Error: Invalid input (" + str(err) + ")\n", file=sys.stderr)
        usage()
        sys.exit(5)

    # Load packet names
    if wiki_links:
        from vitrine.wiki import CoalitionWiki
        wiki = CoalitionWiki()
    else:
        wiki = None

    # Generate HTML
    html = generate_html(toppings, data, all_data, wiki, highlight, progress_callback)

    # Create full page, if requested
    if not only_body:
        html = embed(resources, html)

    # Output results
    file = open(output, "w")
    file.write(html)
    file.close()

if __name__ == '__main__':
    main()
