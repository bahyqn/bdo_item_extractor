import importlib
import xml.etree.ElementTree as ET
import os
from extract.__init import ItemClass
from utils import create_json_class2json, get_all_files, insert_index_categories, insert_index_search, list_manufacture_action, read_json, split_and_clean_text, remove_double_braces, create_json, classify, check_key
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

def create_mapping_file(filename: str, lang: str, file_path: str, save_path:str) -> None:
    temp_context: dict[str, any] = {}

    context = recipe_export(os.path.join(file_path, filename))

    for el in context['string']:
        temp_context[el['index'].strip()] = el['name'].strip()
    create_json(os.path.join(save_path, lang), 'string', temp_context)

def main(data_path: str, save_path: str, default_lang: str) -> None:
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
    
    # index_action_string_path: str = './action_string.json'
    try:
        index_search: dict = {}
        index_categories: dict[str, ItemClass] = {}
        current_lang: str = ''
        manufacture_action_set_dict: dict = {}

        files = get_all_files(data_path)

        for index in trange(len(files)):
            file = files[index]
            '''
            _de_292.xml: ['', 'de', '292.xml']
            292.xml: ['292.xml']
            '''
            split_filename = file.split('_')

            if len(split_filename) == 3:
                current_lang = split_filename[1]
            elif len(split_filename) == 1:
                current_lang = default_lang

            if split_filename[-1] == 'string.xml':
                create_mapping_file(split_filename[-1], default_lang, data_path, save_path)
                continue

            item_data = recipe_export(os.path.join(data_path, file))

            insert_index_search(index_search, current_lang, item_data)
            create_json(os.path.join(save_path, current_lang), split_filename[-1].split('.')[0], item_data)
            insert_index_categories(list(item_data.keys()), index_categories, item_data, current_lang, classify)

        #     list_manufacture_action(os.path.join(data_path, file), manufacture_action_set_dict, current_lang)
        # create_json('', 'action_string', manufacture_action_set_dict)

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
    # save_path = r'E:\projects\others\bdo_database_capture\json'
    save_path: str = './json'
    default_lang: str = 'en'
    data_path = r'E:\paz_extract\ui_data\ui_html\xml\en'
    # save_path = r'E:\projects\others\bdo_database_capture\json'
    main(data_path, save_path, default_lang)