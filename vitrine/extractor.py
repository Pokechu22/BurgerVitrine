# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

from StringIO import StringIO

from solum import JarFile

import os

try:
    from PIL import Image
except:
    try:
        from Imaging import Image
    except:
        Image = None


PATHS = {"terrain": "terrain.png",
         "items": "gui/items.png"}


def extract(jar, file, output, data):
    if Image is None:
        print "Extracting textures requires PIL"
        return

    try:
        jar = JarFile(jar)
    except:
        print "Opening jar file failed"
        return
    if not PATHS[file] in jar.zp.namelist():
        return extract_indivdual(jar, file, output, data)
    path = PATHS[file]
    data = jar.zp.read(path)

    image = Image.open(StringIO(data))
    image.resize((512, 512)).save(output, format="PNG")

    return True


def extract_indivdual(jar, file, output, data):
    if not data:
        print "Error: Vitrine expects Burger output via stdin."
        return False

    if file == "items":
        return extract_indivdual_items(jar, output, data)
    else:
        return extract_indivdual_blocks(jar, output, data)


def extract_indivdual_items(jar, output, data):
    items = {}
    for item in data[0]['items']['item'].itervalues():
        items[item['numeric_id']] = item['text_id']

    img = combine_textures(jar, items, "assets/minecraft/textures/items")
    img.save(output, format="PNG")

    return True


def extract_indivdual_blocks(jar, output, data):
    blocks = {}
    for block in data[0]['blocks']['block'].itervalues():
        blocks[block['numeric_id']] = block['text_id']

    img = combine_textures(jar, blocks, "assets/minecraft/textures/blocks")
    img.save(output, format="PNG")

    return True


def combine_textures(jar, textures, location):
    image = Image.new("RGBA", ((max(textures.iterkeys()) + 1) * 16, 16))
    for id_, texture in textures.iteritems():
        path = "%s/%s.png" % (location, texture)
        if path not in jar.zp.namelist():
            start = "%s/%s_" % (location, texture)
            for path in reversed(jar.zp.namelist()):
                if path.startswith(start) and path.endswith(".png"):
                    break
            else:
                continue

        texture_img = Image.open(StringIO(jar.zp.read(path))).convert("RGBA")
        image.paste(texture_img, (id_ * 16, 0), texture_img)

    return image.resize(tuple(s * 2 for s in image.size))

def grab_block_sprites(jar, data, resources):
    try:
        jar = JarFile(jar)
    except:
        print "Opening jar file failed"
        return

    if not os.path.isdir(resources + "blocks"):
        os.makedirs(resources + "blocks")
    for block in data['blocks']['block'].itervalues():
        if "text_id" in block:
            path = "assets/minecraft/textures/blocks/%s.png" % block["text_id"]
            out_path = resources + "blocks/%s.png" % block["text_id"]
            if path in jar.zp.namelist():
                image = jar.zp.read(path)
                file = open(out_path, 'wb')
                file.write(image)
                file.close()
                block['has_image'] = True
    if not os.path.isdir(resources + "items"):
        os.makedirs(resources + "items")
    for item in data['items']['item'].itervalues():
        if "text_id" in block:
            path = "assets/minecraft/textures/items/%s.png" % item["text_id"]
            out_path = resources + "items/%s.png" % item["text_id"]
            if path in jar.zp.namelist():
                image = jar.zp.read(path)
                file = open(out_path, 'wb')
                file.write(image)
                file.close()
                block['has_image'] = True