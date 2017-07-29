import os
import random
import string
import zipfile

from lxml import etree
import six


RANDOM_STRING_LENGTH = 10


def random_string():
    """Generates string with random ASCII characters."""
    rand_chars = tuple(random.choice(string.ascii_letters + string.digits) for _ in
                       six.moves.range(RANDOM_STRING_LENGTH))
    return ''.join(rand_chars)


def unique_id(zip_num, xml_num):
    """Generate unique random ID.
    :param zip_num: number of .zip archive
    :param xml_num: number of .xml file
    :return: string
    """
    return '_'.join((random_string(),
                     six.text_type(zip_num + 1),
                     six.text_type(xml_num + 1)))


def generate_xml_tree(zip_num, xml_num):
    """Generate ElementTree with following structure:
        <root>
            <var name='id' value='unique random string'>
            <var name='level' value='random int from 1 to 100'>
            <objects>
                <object name='random string'>
            ...
            </objects>
        </root>
    :param zip_num: number of .zip archive
    :param xml_num: number of .xml file
    :return: etree.ElementTree
    """
    level = random.randint(1, 100)
    id = unique_id(zip_num, xml_num)
    root = etree.Element('root')
    root.append(etree.Element('var', name='id', value=id))
    root.append(etree.Element('var', name='level', value=six.text_type(level)))
    objects = etree.SubElement(root, 'objects')
    object_tag_count = random.randint(1, 10)
    for _ in six.moves.range(object_tag_count):
        rand_name = random_string()
        objects.append(etree.Element('object', name=rand_name))
    return etree.ElementTree(root)


def generate_zip_archives(directory, zip_count, xml_count):
    """Generate .zip archives an write .xml files to them.
    :param directory: string directory (may not exists)
    :param zip_count: int how many .zip archives to generate
    :param xml_count: int how many .xml files per archive to generate
    """
    if not os.path.isdir(directory):
        os.makedirs(directory)
    for arch_num in six.moves.range(zip_count):
        arch_name = os.path.join(directory, "Archive-{}.zip".format(arch_num + 1))
        with zipfile.ZipFile(arch_name, 'w') as archive:
            for xml_num in six.moves.range(xml_count):
                xml_name = 'file-{}.xml'.format(xml_num + 1)
                xml_tree = generate_xml_tree(arch_num, xml_num)
                archive.writestr(xml_name, etree.tostring(xml_tree, pretty_print=True))
