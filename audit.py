def is_street_name(elem):
    if elem.attrib['k'] == 'addr:street':
        update_name(elem)
    if elem.attrib['k'] == 'name':
        update_name(elem)
    if elem.attrib['k'] == 'tiger:name_type':
        update_name(elem)
    if elem.attrib['k'] == 'tiger:name_type_1':
        update_name(elem)

def update_name(tag):

    names = ['Adventures', 'Avenue', 'Basin', 'Cabin', 'Campsite', 'Circle', 'Court', 'Creek', 'Drive', 'Lake', 'Lane',
             'Lodge', 'Loop', 'Park', 'Parkway', 'Point', 'Ranch', 'Ridge', 'River', 'Road', 'Stream', 'Street',
             'Trail', 'Trailhead', 'Volcano', 'Way']

    mapping = {'Ave': 'Avenue', 'Cir': 'Circle', 'Ct': 'Court', 'Dr': 'Drive', 'Ln': 'Lane', 'Pky': 'Parkway',
               'Rd': 'Road', 'Trl': 'Trail'}

    name = tag.attrib['v'].title()

    last_word = name.split()[-1]

    for key, value in mapping.items():
        if last_word == key:
            last_word = value
        if last_word != key:
            for word in names:
                if last_word == word:
                    pass
                if last_word != word:
                    pass

    new_name = name.replace(name.split()[-1], last_word)
    tag.set('v', new_name)

    return tag


