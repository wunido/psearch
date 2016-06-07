
leagues = (
        ('Hardcore', 'Hardcore'),
        ('Standard', 'Standard'),
        ('Prophecy', 'Prophecy'),
        ('Prophecyhc', 'Prophecy HC'),
)

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
item = (
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


def mapping_write(request):
    """ Mapping export to file (request - mapping of mod group / saved file - 'mod group'.txt) """
    import urllib
    import os

    url = 'http://api.exiletools.com/endpoints/mapping?field=%s' % request
    response = urllib.request.urlopen(url)

    with open(request+'.txt', 'wb') as file:
        for line in response:
            file.write(line)
    # removing file if empty
    if os.stat(request+'.txt').st_size == 0:
        os.remove(request+'.txt')


def mapping_tuple(request):
    """ Converting mapping into tuple (request - mapping of mod group, not file!) """
    modListFull = [None, ]
    modListNames = [None, ]
    length = len(request)
    with open(request+'.txt', 'r') as file:
        for line in file:
            string = line[length + 1:].strip('\n')
            modListFull.append(line.strip('\n'))
            modListNames.append(string)
    search_form = tuple(zip(modListFull, modListNames))
    return search_form
