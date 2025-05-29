import importlib
import xml.etree.ElementTree as ET
import os
from extract.__init import ItemClass
from utils import create_json_class2json, get_all_files, insert_index_categories, insert_index_search, split_and_clean_text, remove_double_braces, create_json, classify, check_key
from pathlib import Path
from tqdm.rich import trange


def recipe_export(xml_file) -> dict:
    try:
        data: dict[str, any] = {}
        root = ET.parse(xml_file).getroot()
        data['xml'] = root.tag

        if root.tag == 'itemInfo':
            md = importlib.import_module('extract.itemInfo')
        elif root.tag == 'itemmaking' or root.tag == 'productNote':
            md = importlib.import_module('extract.itemmaking')

        for tag in root:
            func = getattr(md, f"{tag.tag}")

            if isinstance(func(tag), list):
                if check_key(classify, tag.tag)not in data:
                    data[check_key(classify, tag.tag)] = []

                data[check_key(classify, tag.tag)].extend(func(tag))

            else:
                data[check_key(classify, tag.tag)] = func(tag)

        return data
    except ET.ParseError as e:
        print(f"Error parsing {xml_file}: {e}")

def main(data_path: str, save_path: str, default_server: str):
    '''
    index_search:
        'en': {
            '292': 'Flare of the Ancients',
            ...
        },
        'sp': {
            ...
        }
    '''
    try:
        index_search: dict = {}
        index_categories: dict[str, ItemClass] = {}

        files = get_all_files(data_path)

        for index in trange(len(files)):
            file = files[index]
            '''
            _de_292.xml: ['', 'de', '292.xml']
            292.xml: ['292.xml']
            '''
            temp_server = file.split('_')

            # print(file)
            item_data = recipe_export(os.path.join(data_path, file))

            if len(temp_server) == 3:
                # print(f"path: {os.path.join(data_path, temp_list[1])}")
                # print(f"server: {temp_list[1]}")
                insert_index_search(index_search, temp_server[1], item_data)
                create_json(os.path.join(save_path, temp_server[1]), temp_server[-1].split('.')[0], item_data)
                insert_index_categories(list(item_data.keys()), index_categories, item_data, temp_server[1], classify)
            elif len(temp_server) == 1:
                # print(f"path: {os.path.join(data_path, temp_list[0])}")
                # print(f"server: {default_server}")
                insert_index_search(index_search, default_server, item_data)
                create_json(os.path.join(save_path, default_server), temp_server[-1].split('.')[0], item_data)
                insert_index_categories(list(item_data.keys()), index_categories, item_data, default_server, classify)

        for el in index_search:
            create_json(os.path.join(save_path, el), f"{el}_index_search", index_search[el])
            create_json_class2json(os.path.join(save_path, el), f"{el}_index_categories", index_categories[el])

    except FileNotFoundError as e:
        print('File not found.')
    except NotADirectoryError as e:
        print('data_path is a folder!!!')
    except PermissionError as e:
        print('Required administrator!!!')
    except OSError as e:
        print('The path is invalid!!!')


if __name__ == '__main__':
    '''
    data_path = r''
    '''
    # data_path: str = './xml'
    save_path: str = './json'
    default_server: str = 'en'
    data_path = r'E:\paz_extract\ui_data\ui_html\xml\en'
    # save_path = r'E:\projects\others\bdo_database_capture\json'
    main(data_path, save_path, default_server)