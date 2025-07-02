import json
import os
import re
from functools import wraps
from extract.__init import ItemClass
from pathlib import Path
import xml.etree.ElementTree as ET


classify = {
            'shop': 'Shop',
            'node': 'Node',
            'cook': 'Cooking',
            'house': 'House',
            'alchemy': 'Alchemy',
            'fishing': 'Fishing',
            'collect': 'Gathering',
            'makelist': 'Makelist',
            'manufacture': 'Processing',
        }

def convert_escaped_newlines(func):
    @wraps(func)
    def wrapper(text: str, *args, **kwargs):
        return func(text.replace('\\n', '\n'), *args, **kwargs)
    return wrapper


@convert_escaped_newlines
def split_and_clean_text(text: str, delimiter: str = '\n') -> list[str]:
    """
    Splits the input text using the specified delimiter while preserving the original format.
    Removes empty lines from the result.
    
    :param text: The input string to be processed.
    :param delimiter: The delimiter used to split the text (default is '\n').
    :return: A list of non-empty strings after splitting.
    """
    # cleaned_text = re.sub(r'^\n+$', text, delimiter)
    return [line.strip() for line in text.split(delimiter) if line.strip()]


@convert_escaped_newlines
def remove_double_braces(text: str, delimiter: str = '\n'):
    '''
    before:
        - Crafting Method: Processing ({KeyBind:Manufacture}) - Simple Alchemy
    
    after:
        - Crafting Method: Processing - Simple Alchemy
    '''
    return re.sub(r'\s*\(\{KeyBind:[^\}]+\}\)', '', text)

@convert_escaped_newlines
def remove_double_braces_to_list(text: str, delimiter: str = '\n'):
    '''
    before:
        - Crafting Method: Processing ({KeyBind:Manufacture}) - Simple Alchemy
    
    after:
        - Crafting Method: Processing
        - Simple Alchemy
    '''
    cleaned_text = re.sub(r'\s*\(\{KeyBind:[^\}]+\}\)', '', text)
    temp = [line.strip() for line in cleaned_text.split(delimiter) if line.strip()]
    if len(temp) == 0:
        return ''
    elif len(temp) == 1:
        return temp[0]
    else:
        return temp


def check_key(ck_dict: dict, tag: str) -> str:
    return ck_dict.get(tag) if ck_dict.get(tag) else tag

def create_json(path: str, item_key: str, data: dict | object):
    save_file_path = os.path.join(path, item_key+'.json')
    if path:
        os.makedirs(path, exist_ok=True)

    with open(save_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        # print(save_file_path + ' created.')

def create_json_class2json(path: str, item_key: str, data: object):
    save_file_path = os.path.join(path, item_key+'.json')
    os.makedirs(path, exist_ok=True)

    with open(save_file_path, "w", encoding="utf-8") as f:
        f.write(data.model_dump_json(indent=4))


def get_all_files(folder_path: str):
    folder = Path(folder_path)
    files = [file.name for file in folder.iterdir() if file.is_file()]
    # print(f'len: {len(files)}')
    return files

def insert_index_search(dic: dict, server: str, data: dict) -> None:
    if data['xml'] == 'itemInfo':
        if not dic.get(server):
        #     dic[server] = []
        # dic[server].append({
        #     'id': data.get('itemKey'),
        #     'item': data.get('itemName'),
        #     'img': data.get('itemIcon')
        # })
            dic[server] = {}
        dic[server][str(data.get('itemKey'))] = {
            'id': data.get('itemKey'),
            'value': data.get('itemName'),
            'img': data.get('itemIcon')
        }

def insert_index_categories(tag_list: list, class_dict: dict, data: dict, server: str, classify: dict) -> None:
    '''
    ['manufacture', 'makelist']
    ['makelist']
    logic: 
        xml == 'itemInfo'
            如果lis中只有1个 element, 
            判断这个element是不是makelist,是就放在makelist类别
            不是就放在对应的类别

            如果lis中有 severral 个 element, 逐一添加类别, 遇到 makelist 则不添加

    '''
    if data.get('xml') == 'itemInfo':
        if not class_dict.get(server):
            class_dict[server] = ItemClass()

        # classify = {
        #     'shop': 'Shop',
        #     'node': 'Node',
        #     'cook': 'Cooking',
        #     'house': 'House',
        #     'alchemy': 'Alchemy',
        #     'fishing': 'Fishing',
        #     'collect': 'Gathering',
        #     'makelist': 'Makelist',
        #     'manufacture': 'Processing',
        # }
        temp = tag_list[5:]
        # print(tag_list)
        # print(temp)

        if len(temp) == 1:
            cl = classify.get(temp[0])
            class_dict[server][temp[0]].append({
                'itemKey': data.get('itemKey'),
                'itemName': data.get('itemName'),
                'itemIcon': data.get('itemIcon'),
            })
        else:
            for el in tag_list[5:]:
                if el != 'Makelist':
                    class_dict[server][el].append({
                        'itemKey': data.get('itemKey'),
                        'itemName': data.get('itemName'),
                        'itemIcon': data.get('itemIcon') or '',
                    })

def list_manufacture_action(xml_file: str, manufacture_action_set_dict: dict, lang: str) -> None:
    if lang not in manufacture_action_set_dict:
        manufacture_action_set_dict[lang] = {}

    root = ET.parse(xml_file).getroot()
    for el in root.findall('manufacture'):
        action = el.attrib.get('action', 'unknown')
        if action != 'unknown' and action not in manufacture_action_set_dict[lang]:
            manufacture_action_set_dict[lang][action] = {
                'itemKey': root.find('itemKey').text,
                'itemName': root.find('itemName').text,
                'manufacture': el.attrib.get('action', 'unknown')
            }

def read_json(path: str) -> dict | list:
    with open(path, mode='r', encoding='utf-8') as f:
        return f.read()