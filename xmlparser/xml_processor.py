from concurrent import futures
import csv
import os
import zipfile

import lxml


ZIP_EXTENSION = '.zip'
XML_EXTENSION = '.xml'


class NoSuchDirectoryException(Exception):
	"""Exception raised when directory doesn't exist."""


def parse_xml(content, id_level_file, id_objects_file):
    """Parse xml and save data to .csv files.
    :param content: content of xml file
    :param id_level_file: file to save id-level mapping to.
    :param id_objects_file: file to save id-objects mapping to.
    """
    root = lxml.etree.fromstring(content)
    id = root[0].get('value')
    level = root[1].get('value')
    return id, level, tuple(obj.get('name') for obj in root[2])


def process_archive(directory, arch_name, id_level_file, id_objects_file):
    """Opens archive and parse .xml files in it.
    :param directory: directory where archive is located
    :param arch_name: name of archive
    :param id_level_file: file to save id-level mapping to.
    :param id_objects_file: file to save id-objects mapping to.
    """
    result = []
    try:
        with zipfile.ZipFile(
                os.path.join(directory, arch_name)) as archive:
            for xml_name in archive.namelist():
                if xml_name.endswith(XML_EXTENSION):
                    try:
                         result.append(parse_xml(archive.read(xml_name),
                                                 id_level_file,
                                                 id_objects_file))
                    except lxml.etree.ParseError:
                        print("Cannot parse XML: {}".format(xml_name))
    except zipfile.BadZipfile:
        print("Cannot open ZIP file: {}".format(arch_name))
    return result


def process_zip_archives(directory, id_level_file, id_objects_file):
    """Process all .zip files in given directory.
    :param directory: directory where archives are located
    :param id_level_file: file to save id-level mapping to.
    :param id_objects_file: file to save id-objects mapping to.
    """
    if os.path.isdir(directory):
        futures_list = []
        with futures.ProcessPoolExecutor() as executor:
            for arch_name in os.listdir(directory):
                if arch_name.endswith(ZIP_EXTENSION):
                    future = executor.submit(process_archive,
                                             directory,
                                             arch_name,
                                             id_level_file,
                                             id_objects_file)
                    futures_list.append(future)
            with open(id_level_file, 'a') as csv1:
                id_level_writer = csv.writer(csv1)
                with open(id_objects_file, 'a') as csv2:
                    id_objects_writer = csv.writer(csv2)
                    for f in futures.as_completed(futures_list):
                        data = f.result()
                        for item in data:
                            id_level_writer.writerow((item[0], item[1]))
                            for obj in item[2]:
                                id_objects_writer.writerow((item[0], obj))
    else:
        raise NoSuchDirectoryException("No such directory: {}".format(directory))
