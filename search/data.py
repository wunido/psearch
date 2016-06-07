
leagues = (
        ('Hardcore', 'Hardcore'),
        ('Standard', 'Standard'),
        ('Prophecy', 'Prophecy'),
        ('Prophecyhc', 'Prophecy HC'),
)


def item_type():
    # creating dicts of items
    itemType = 'attributes.itemType'
    equipType = 'attributes.equipType'

    body_armour = {itemType: 'Body'}
    boots = {itemType: 'Boots'}
    gloves = {itemType: 'Gloves'}
    helmet = {itemType: 'Helmet'}
    shield = {itemType: 'Shield'}
    quiver = {itemType: 'Quiver'}
    card = {itemType: 'Card'}
    flask = {itemType: 'Flask'}
    gem = {itemType: 'Gem'}
    jewel = {itemType: 'Jewel'}
    amulet = {itemType: 'Amulet'}
    belt = {itemType: 'Belt'}
    ring = {itemType: 'Ring'}
    maps = {itemType: 'Map'}
    bow = {itemType: 'Bow'}
    wand = {itemType: 'Wand'}

    oh_weapon = {equipType, 'One Handed Melee Weapon'}
    th_weapon = {equipType, 'Two Handed Melee Weapon'}

    oh_sword = {itemType: 'Sword', equipType: 'One Handed Melee Weapon'}
    th_sword = {itemType: 'Sword', equipType: 'Two Handed Melee Weapon'}
    oh_axe = {itemType: 'Axe', equipType: 'One Handed Melee Weapon'}
    th_axe = {itemType: 'Axe', equipType: 'Two Handed Melee Weapon'}
    oh_mace = {itemType: 'Mace', equipType: 'One Handed Melee Weapon'}
    th_mace = {itemType: 'Mace', equipType: 'Two Handed Melee Weapon'}

    # creating list of tuples for form
    itemform = (
            (None, 'None'),
            (body_armour, 'Body Armour'),
            (boots, 'Boots'),
            (gloves, 'Gloves'),
            (helmet, 'Helmet'),
            (shield, 'Shield'),
            (quiver, 'Quiver'),
            (card, 'Card'),
            (flask, 'Flask'),
            (gem, 'Gem'),
            (jewel, 'Jewel'),
            (amulet, 'Amulet'),
            (belt, 'Belt'),
            (ring, 'Ring'),
            (maps, 'Map'),
            (bow, 'Bow'),
            (wand, 'Wand'),
            (oh_weapon, 'Generic One Handed Weapon'),
            (th_weapon, 'Generic Two Handed Weapon'),
            (oh_sword, 'One Handed Sword'),
            (th_sword, 'Two Handed Sword'),
            (oh_axe, 'One Handed Axe'),
            (th_axe, 'Two Handed Axe'),
            (oh_mace, 'One Handed Mace'),
            (th_mace, 'Two Handed Mace'),
    )
    return itemform


class Mapping:
    """ Mapping export to file (need input - 'mod group' / saved file - 'mod group'.txt) """
    def __init__(self, modtype):
        self.modtype = modtype

    def mapping_write(self):
        import urllib
        import os

        url = 'http://api.exiletools.com/endpoints/mapping?field=%s' % self.modtype
        response = urllib.request.urlopen(url)

        with open(self.modtype+'.txt', 'wb') as file:
            for line in response:
                file.write(line)
        # removing file if empty
        if os.stat(self.modtype+'.txt').st_size == 0:
            os.remove(self.modtype+'.txt')


def mapping_tuple(modtype):
    """ Converting mapping into tuple (request - mapping of mod group, not file!) """
    modListFull = [None, ]
    modListNames = [None, ]
    length = len(modtype)
    with open(modtype+'.txt', 'r') as file:
        for line in file:
            string = line[length + 1:].strip('\n')
            modListFull.append(line.strip('\n'))
            modListNames.append(string)
    search_form = tuple(zip(modListFull, modListNames))
    return search_form


def search_form_full():
    """ creating full search form from mapping tuples (multiple files) /need to create """


def convert_resp(request):
    """ converting json input into dict with chosen data """
    item_data = {}
    for hit in request['hits']['hits']:
        item_id = hit["_source"]["uuid"]
        full_name = hit["_source"]["info"]["fullName"]
        seller_account = hit["_source"]["shop"]["sellerAccount"]
        if 'chaosEquiv' in hit["_source"]["shop"].keys():
            chaos_equiv = hit["_source"]["shop"]["chaosEquiv"]
        else:
            chaos_equiv = 'no price'
        if 'modsTotal' in hit["_source"].keys():
            mods_total = hit["_source"]["modsTotal"]
        else:
            mods_total = None

        # adding results to item_data
        item_data[item_id] = {'full_name': full_name,
                              'chaos_equiv': chaos_equiv,
                              'seller_account': seller_account,
                              'mods_total': mods_total}
    return item_data
