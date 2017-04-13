# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

from .topping import Topping


class RecipesTopping(Topping):
    KEY = "recipes"
    NAME = "Recipes"
    NO_ESCAPE = ("json")
    SORING = Topping.NUMERIC_SORT
    PRIORITY = 8

    def _get_entry_html(self, entry, key=None):
        if entry is None or len(entry) == 0:
            return '<div class="no entry"></div>'
        else:
            id = key
            aggregate = '<a id="%s"></a>' % self.anchor(id)
            for recipe in entry:
                aggregate += self._entry(self.parse_entry(recipe, key),
                                         self._get_dl(recipe), False)
            return aggregate

    def _entry(self, title, content, escape=True):
        if escape:
            title = self.escape(title)
        return ('<div class="entry">' +
                '<div class="workbench"><div class="craftgrid">' +
                '%s</div><div class="result">%s</div></div></div>') % (
                    content, title
                )

    def _split(self, left, right):
        return ('<div class="split"><div class="left">%s</div>' +
                '<div class="right">%s</div></div>') % (left, right)

    def parse_entry(self, entry, key):
        result = self.craft_item(entry["makes"])
        aggregate = ""
        if entry["type"] == "shape":
            materials = {' ': '<div class="empty"></div>'}
            for key, item in entry["raw"]["subs"].iteritems():
                materials[key] = self.craft_item(item)
            rows = entry["raw"]["rows"]
            for i in range(3 - len(rows)):
                rows.append("   ")
            for row in rows:
                while len(row) < 3:
                    if len(row) % 2 == 0:
                        row += ' '
                    else:
                        row = ' ' + row
                aggregate += '<div class="craftrow">'
                for col in row:
                    aggregate += materials[col]
                aggregate += "</div>"
        else:
            aggregate += '<div class="craftrow">'
            i = 0
            while len(entry["ingredients"]) < 9:
                entry["ingredients"].append(None)
            for material in entry["ingredients"]:
                aggregate += self.craft_item(material)
                i += 1
                if i % 3 == 0:
                    aggregate += '</div><div class="craftrow">'
            aggregate += "</div>"
            #aggregate += "(shapeless)"
        if "id" in entry:
            aggregate += entry["id"]

        entry["json"] = aggregate
        return result

    def craft_item(self, item):
        if item is None or "data" not in item:
            return '<div class="empty"></div>'

        material = item["data"]
        if "display_name" in material:
            title = material["display_name"]
        elif "name" in material:
            title = material["name"]
        elif "text_id" in material:
            title = material["text_id"]
        else:
            title = "Unknown"

        if "numeric_id" in material:
            content = material["numeric_id"]
            class_ = "craftitem large" if content < 100 else "craftitem"
        elif "text_id" in material:
            content = material["text_id"]
            class_ = "craftitem"
        else:
            content = material
            class_ = "craftitem"
        result = '<div title="%s" class="%s">%s' % (title, class_, content)

        if "count" in item and item["count"] > 1:
            result += '<div class="amount">%s</div>' % item["count"]
        if "metadata" in item:
            result += '<div class="metadata">%s</div>' % item["metadata"]

        result += '</div>'
        return result
