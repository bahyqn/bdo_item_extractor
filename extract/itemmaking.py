# itemmaking.xml
def nodeProduct(tag) -> list:
    return get_attrib(tag)

def fishing(tag) -> list:
    return get_attrib(tag)

def alchemy(tag) -> list:
    return get_attrib(tag)

def cooking(tag) -> list:
    return get_attrib(tag)

def manufacture(tag) -> list:
    return get_attrib(tag)

def houseCraft(tag) -> list:
    return get_attrib(tag)

def collect(tag) -> list:
    return get_attrib(tag)

# string.xml
def string(tag) -> list:
    data: list = []
    for el in tag.findall('message'):
        data.append({
            'index': el.attrib.get('index', 'unknown'),
            'name': el.attrib.get('name', 'unknown')
        })
    return data

def get_attrib(tag) -> list:
    data: list = []
    for el in tag.findall('item'):
        data.append({
            'key': el.attrib.get('key', 'unknown'),
            'name': el.attrib.get('name', 'unknown'),
            'icon': el.attrib.get('icon', 'unknown'),
        })
    return data