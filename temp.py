from argparse import Action
from gettext import find
import importlib
import os
from pathlib import Path
from plistlib import FMT_XML
import sys
from typing import Counter
from utils import create_json, get_all_files, remove_double_braces
import xml.etree.ElementTree as ET


def find_label(xml_file: str, label: str, attrib: str='', several: bool=False) -> None:
    '''
    mainusage: find label
    several = True: not support attrib
    '''
    def is_attrib(el, attrib):
        ac = el.attrib.get(attrib, 'unknown')
        if ac and ac != 'unknown':
            print(xml_file)
            temp = " ".join([s.capitalize() for s in ac.split('_')[1:]])
            print(ac, temp)

    try:
        root = ET.parse(xml_file).getroot()
        # print([el.tag for el in root])
        
        for el in root:
            if el.tag == label:
                counter = Counter([el.tag for el in root])
                # print(counter)

                if several:
                    if counter[label] > 1:
                        print(xml_file, counter[label])
                        is_attrib(el, attrib)
                        break
                else:
                    print(f"{xml_file}, counter: {counter[label]}")
                    break
                
                if attrib:
                    ac = el.attrib.get(attrib, 'unknown')
                    if ac and ac != 'unknown':
                        print(xml_file)
                        temp = " ".join([s.capitalize() for s in ac.split('_')[1:]])
                        print(temp)
    except ET.ParseError as e:
        print(f"Error parsing {xml_file}: {e}")

def find_item(xml_file, flag: str=''):
    try:
        root = ET.parse(xml_file).getroot() # 使用 folder_path
        # print(root.tag)
        itemName = root.find('itemName')

        if (itemName is not None) and (itemName.text.lower().find(flag.lower()) != -1):
            print(f"item: {flag}")
            print(f"{os.path.join(folder_path, xml_file)} ------------------> {itemName.text}")
            sys.exit(0)
    except ET.ParseError as e:
        print(f"Error parsing {xml_file}: {e}")

def extract_structure(xml_file, structure):
    '''
    It can only be used to get the parent label and sub-label.
    If you want to know the complete structure, please run find_label() and view the file.
    '''

    def recursive_build(element, current_dict, current_xml):
        tag = element.tag
        # print(f"file: {current_xml}")
        # print(f"structure: {current_dict}")
        # print(f"tag: {tag}")

        # if tag == 'house':
        #     print(xml_file)
            # sys.exit(0)

        if tag not in current_dict:
            current_dict[tag] = {}
            if element.attrib:
                current_dict[tag] = {
                    'attrib': element.attrib
                }

        for child in element:
            recursive_build(child, current_dict[tag], current_xml)
        

    try:
        root = ET.parse(os.path.join(folder_path, xml_file)).getroot()
        recursive_build(root, structure, xml_file)
    except ET.ParseError as e:
        print(f"Error parsing {xml_file}: {e}")

    return structure

def get_xml_data(xml_file):
    try:
        data: dict[str, any] = {}
        root = ET.parse(xml_file).getroot()

        if root.tag == 'itemInfo':
            md = importlib.import_module('extract.itemInfo')
        elif root.tag == 'itemmaking' or root.tag == 'productNote':
            md = importlib.import_module('extract.itemmaking')

        for tag in root:
            func = getattr(md, f"{tag.tag}")

            if isinstance(func(tag), list):
                if tag.tag not in data:
                    data[tag.tag] = []
                data[tag.tag].extend(func(tag))
            else:
                data[tag.tag] = func(tag)
        print(data['itemDesc'])
        create_json('./json/', '4051', data)
    except ET.ParseError as e:
        print(f"Error parsing {xml_file}: {e}")

def main():
    ...
    
if __name__ == '__main__':
    folder_path = 'E:/paz_extract/ui_data/ui_html/xml/en'
    # folder_path = './xml'
    structure_file = './structure/json'
    index_file = './index.json'
    files = get_all_files(folder_path)

    metadata: dict = {}

    # tempx = r'E:/paz_extract/ui_data/ui_html/xml/en\4051.xml'
    # get_xml_data(tempx)

    for file in files:
        # get_xml_data(os.path.join(folder_path, file))

        temp_file = file.split('_')
        if len(temp_file) == 1:
            # get_xml_data(os.path.join(folder_path, temp_file[0]))
            # find_item(os.path.join(folder_path, file), 'Melted Iron Shard')
            # find_item(os.path.join(folder_path, file), 'Mudskipper')
            find_item(os.path.join(folder_path, file), 'Master Matchlock')

            # find_label(xml_file=os.path.join(folder_path, temp_file[0]), label='manufacture', several=True)
            
            # makelist
            # find_label(xml_file=os.path.join(folder_path, temp_file[0]), label='makelist')
    #         metadata = extract_structure(os.path.join(folder_path, temp_file[0]), metadata)
    # print(metadata)