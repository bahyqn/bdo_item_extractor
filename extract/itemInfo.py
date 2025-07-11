from utils import remove_double_braces, deduplicate_list
import xml.etree.ElementTree as ET

def itemKey(tag) -> int:
    return tag.text

def itemName(tag) -> str:
    return tag.text

def itemIcon(tag) -> str:
    return tag.text.lower() 

def itemDesc(tag) -> str:
    return tag.text.replace('\\n', '\n')

def house(tag) -> list:
    data: dict[str, any] = {
        'type': tag.attrib.get("type"),
        'item': []
    }
    house = tag.findall('item')
    for el in house:
        data['item'].append(get_items(el))
    return deduplicate_list([data])

def makelist(tag) -> list:
    data: list = []
    for item in tag.findall('item'):
        data.append(get_items(item))
    return data

def manufacture(tag) -> list:
    data = {
        'action': tag.attrib.get("action", "Unknown"),
        'item': []
    }

    for item in tag.findall('item'):
        data['item'].append(get_items(item))
    return deduplicate_list([data])


def alchemy(tag) -> list:
    data: list = []
    for item in tag.findall('item'):
        data.append(get_items(item))
    return deduplicate_list([data])

def cook(tag) -> list:
    data: list = []
    for item in tag.findall('item'):
        data.append(get_items(item))
    return deduplicate_list([data])

def shop(tag) -> list:
    return [tag.find('character').find('name').text]

def collect(tag) -> list:
    return [tag.find('character').find('name').text]

def node(tag) -> list:
    return [tag.attrib.get("region", "Unknown")]

def fishing(tag) -> int:
    return 1

def get_items(tag):
    data: dict[str, any] = {
        'id': tag.find('id').text,
        'name': tag.find('name').text,
        'icon': tag.find('icon').text,
        'desc': remove_double_braces(tag.find('desc').text),
    }
    try:
        count = tag.find('count')
        
        if count is not None:
            data['count'] = count.text
    except ET.ParseError as e:
        ...
    return data