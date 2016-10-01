# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

import os
import sys
import getopt
import json


def usage():
    print "Usage:"
    print "  vitrine.py [-b] [-w] [-r file] [-o file]"
    print "  vitrine.py -i | -t file [-o file]"
    print
    print "Options:"
    print "  -b, --body: Don't generate a complete HTML document"
    print "  -w, --wiki: Add links to the MinecraftCoalition wiki and display packet names"
    print "  -r, --resources file: Path to resources folder"
    print "  -o, --output file: Output result into a file instead of",
    print "standard output"
    print "  -i, --items file: Extract items.png from jar file"
    print "  -t, --terrain file: Extract terrain.png from jar file"
    print "  -h, --help: Show this help"


def import_toppings():
    """
    Attempts to load all available toppings.
    """
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


def embed(html):
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


def generate_html():
    toppings = import_toppings()

    # Load JSON objects from stdin
    if sys.stdin.isatty():
        print "Error: Vitrine expects Burger or Hamburglar output via stdin.\n"
        usage()
        sys.exit(3)

    try:
        data = json.load(sys.stdin)
    except ValueError, err:
        print "Error: Invalid input (" + str(err) + ")\n"
        usage()
        sys.exit(5)

    diff = not isinstance(data, list)
    if not diff:
        data = data[0]

    if sprites:
        from vitrine import extractor
        extractor.grab_block_sprites(jar, data, resources)
    # Load packet names
    if wiki_links:
        from vitrine.wiki import CoalitionWiki
        wiki = CoalitionWiki()
    else:
        wiki = None
        
    # Generate HTML
    aggregate = ""

    for topping in sorted(toppings, key=lambda x: -x.PRIORITY):
        if topping.KEY == None:
            continue
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

        aggregate += str(topping(obj, diff, wiki))

    if not only_body:
        aggregate = embed(aggregate)

    # Output results
    file = open(output, "w")
    file.write(aggregate)
    file.close()


def extract():
    from vitrine import extractor
    print "Extracting"
    data = None
    if not sys.stdin.isatty():
        try:
            data = json.load(sys.stdin)
        except ValueError, err:
            print "Error: Invalid input (" + str(err) + ")\n"
    if not extractor.extract(jar, mode, output, data):
        sys.exit(1)

if __name__ == '__main__':
    try:
        opts, args = getopt.gnu_getopt(
            sys.argv[1:],
            "o:bwi:t:r:s:h",
            [
                "output=",
                "body",
                "items=",
                "terrain=",
                "resources=",
                "sprites=",
                "help"
            ]
        )
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(1)

    # Default options
    output = sys.stdout
    only_body = False
    mode = "html"
    jar = None
    sprites = False
    wiki_links = False
    resources = "resources/"

    for o, a in opts:
        if o in ("-o", "--output"):
            output = a
        elif o in ("-b", "--body"):
            only_body = True
        elif o in ("-w", "--wiki"):
            wiki_links = True
        elif o in ("-r", "--resources"):
            resources = a
            if resources[-1] != "/":
                resources += "/"
        elif o in ("-i", "--items"):
            mode = "items"
            jar = a
        elif o in ("-t", "--terrain"):
            mode = "terrain"
            jar = a
        elif o in ("-s", "--sprites"):
            sprites = True
            jar = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)

    if mode == "html":
        generate_html()
    else:
        extract()
