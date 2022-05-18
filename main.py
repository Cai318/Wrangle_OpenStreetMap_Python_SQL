import os
import audit
import csv
import codecs
import re
import pandas as pd
import xml.etree.cElementTree as ET
import cerberus
import schema

OSM_PATH = 'Sample.osm'

path = "C:\\Users\\CL\\PycharmProjects\\Wrangle"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEM_CHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

def file_sizes(path):
    project_path = lambda x: os.path.isfile(os.path.join(path, x))
    files_list = filter(project_path, os.listdir(path))

    # Creating a list of files and their sizes
    size_of_file = [(f, os.stat(os.path.join(path, f)).st_size) for f in files_list]

    num_list = []
    size_dict = {}
    for f, s in size_of_file:
        num_list.append(round(s / (1024 * 1024)))
        size_dict[f] = round(s / (1024 * 1024), 3)

    size_df = pd.DataFrame(list(size_dict.items()), columns=['FILE NAME', 'FILE SIZE (MB)'])
    size_df = size_df.to_string(index=False)

    print("\nComplete Project Size:\t{} MB\n".format(sum(num_list)))
    print(size_df)

def shape_element(element, node_attr_fields=None, way_attr_fields=None,
                  problem_chars=PROBLEM_CHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    if way_attr_fields is None:
        way_attr_fields = WAY_FIELDS
    if node_attr_fields is None:
        node_attr_fields = NODE_FIELDS

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    if element.tag == 'node':
        node_tags_dict = {} ##
        for attribute in element.attrib:
            if attribute in node_attr_fields:
                node_attribs[attribute] = element.get(attribute)

        for child in element.iter('tag'):
            node_tags_dict['id'] = element.attrib['id'] ##

            for tag_attrib in child.attrib: ##
                if tag_attrib == 'k': ##
                    if LOWER_COLON.search(child.get(tag_attrib)):
                        node_tags_dict['key'] = ':'.join(child.get(tag_attrib).split(':')[1:])
                        node_tags_dict['type'] = child.get(tag_attrib).split(':')[0]
                    elif PROBLEM_CHARS.search(child.get(tag_attrib)):
                        continue
                    else:
                        node_tags_dict['type'] = default_tag_type
                        node_tags_dict['key'] = child.get(tag_attrib)
                if tag_attrib == 'v':
                    node_tags_dict['value'] = child.get(tag_attrib)
            tags.append(node_tags_dict)

        return {'node': node_attribs, 'node_tags': tags}


    elif element.tag == 'way':
        node_dict = {}
        tag_dict = {}
        for attribute in element.attrib:
            if attribute in way_attr_fields:
                way_attribs[attribute] = element.get(attribute)

        for child in element.iter('tag'):
            tag_dict['id'] = element.attrib['id']
            for tag_attrib in child.attrib:
                if tag_attrib == 'k':
                    if LOWER_COLON.search(child.get(tag_attrib)):
                        tag_dict['key'] = ':'.join(child.get(tag_attrib).split(':')[:])
                        tag_dict['type'] = child.get(tag_attrib).split(':')[0]
                    elif PROBLEM_CHARS.search(child.get(tag_attrib)):
                        continue
                    else:
                        tag_dict['type'] = default_tag_type
                        tag_dict['key'] = child.get(tag_attrib)
                if tag_attrib == 'v':
                    tag_dict['value'] = child.get(tag_attrib)
            tags.append(tag_dict)
            tag_dict = {}
        n = 0

        for child in element.iter('nd'):
            node_dict['id'] = element.attrib['id']
            for tag_attrib in child.attrib:
                node_dict['node_id'] = child.get(tag_attrib)
                node_dict['position'] = n
                n += 1
            way_nodes.append(node_dict)

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(iter(validator.errors.items()))
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = print(errors)

        raise Exception(message_string.format(field, error_string))

class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow(row)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w', encoding='utf8') as nodes_file, \
            codecs.open(NODE_TAGS_PATH, 'w', encoding='utf8') as nodes_tags_file, \
            codecs.open(WAYS_PATH, 'w', encoding='utf8') as ways_file, \
            codecs.open(WAY_NODES_PATH, 'w', encoding='utf8') as way_nodes_file, \
            codecs.open(WAY_TAGS_PATH, 'w', encoding='utf8') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for _, element in ET.iterparse(file_in, events=('start',)):
            for tag in element.iter('tag'):
                if element.tag == 'node' or element.tag == 'way':
                    audit.is_street_name(tag)
                if element.tag != 'node' or element.tag != 'way':
                    pass
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])
            element.clear()


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower with full osm.
    # When validating consider first running 'create_sample.py' for a sample sized osm.
    process_map(OSM_PATH, validate=True)
    file_sizes(path)
