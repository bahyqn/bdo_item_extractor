** | [ENGLISH](README.md) | [中文](README_CN.md) | **
# BDO Item Data Extractor
This project extracts item data from Black Desert Online game files. 
<span style="color: red">Tested exclusively on the NA client.</span>

## Prerequisites
* PAZ-Unpacker
* Python (current: 3.12.3)

<span style="color:red; background-color: yellow;font-weight: bold;font-size: 1.5rem">Before you need to know</span>
> PAZ path:
```
Offical website:
    Pearlabyss\BlackDesert\Paz

Steam:
    Steam\steamapps\common\BlackDesert\Paz
```
<span style="color:red; background-color: #87CEFA;font-weight: bold;font-size: 1.5rem">In PAZ-Unpacker</span>
> Game items path:
```
ui_data\ui_html\xml
```

> Icon path:
```
ui_texture\icon\new_icon
ui_texture\icon\new_icon\product_icon_png
```
<span style="color:red; background-color: #87CEFA;font-weight: bold;font-size: 1.5rem">main.py</span>
```
    # data_path = r'E:\ui_html\xml\en'
    # save_path = r'E:\save\ui_data\ui_html\xml\en'
    data_path = r''
    save_path = r''


    There are four languages on the NA client(sp, fr, de, en). 
    This project uses split('_') to distinguish different language files
    _sp_292.xml .split('_') ['', 'sp', '292.xml']
    _fr_292.xml
    _de_292.xml
    292.xml     .split('_') ['292.xml']

    default_server = 'en'
```

## Usage
1. Download PAZ-Unpacker and this project.
2. Open PAZ folder with PAZ-Unpacker.
3. Select and extract.
4. Open this project and run the following commands in the terminal.
   ```
    python -m venv .venv

    .\.venv\Scripts\activate

    pip install pydantic

    python main.py
   ```


# File structure after running main.py
```
|-en
|-fr
|-de
|-sp

-----------------------------------------

|-en/
|--292.json
|--293.json
|-- ...
|--en_index_categories.json
|--en_index_search.json
|-- itemmaking.json
|-- string.json

-----------------------------------------

|- en_index_search.json
{
    "10005": "Azwell Longsword",
    "10006": "Ain Longsword",
    "10007": "Seleth Longsword",
    ...
}

-----------------------------------------

|- en_index_categries.json
{
    "Shop": [
        {
            "itemKey": "10005",
            "itemName": "Azwell Longsword"
        },
        {
            "itemKey": "10006",
            "itemName": "Ain Longsword"
        },
        ...
    ],
    "Node": [
        {
            "itemKey": "4001",
            "itemName": "Iron Ore"
        },
        {
            "itemKey": "4002",
            "itemName": "Lead Ore"
        },
        ...
    ],
    ...
}
```

# xml_label cover to categories （Used in utils.py）
```
xml_label                      categories
shop ------------------------> Shop
node ------------------------> Node
cook ------------------------> Cook
house -----------------------> House
alchemy ---------------------> Alchemy
fishing ---------------------> Fishing
collect ---------------------> Collect
makelist --------------------> Makelist
manufacture -----------------> Processing
```
```


# Game Items Info
```
<itemInfo>
    <itemKey>292</itemKey>
	<itemName>Flare of the Ancients</itemName>
	<itemIcon>00000292.png</itemIcon>
	<itemDesc>A flare that produces an explosion of brilliant light.\n\n- Stuns nearby enemies for a period of time when used in the Altar of Blood.\n※ Has no effect when used outside of Altar of Blood.\n\n- Cooldown: 2 min\n\n- How to Obtain: Process Dim Origin of Clear Water, Dim Origin of Crimson Flame, Dim Origin of Earth, Ancient Spirit Dust x4 using Simple Alchemy.</itemDesc>


    // 6386.xml
    // item: Silk Honey Grass Supplement
    <shop>
        <character>
            <name>Fughar</name>
        </character>
    </shop>
    <shop>
        ...
    </shop>
    ...


    // 820012.xml
    // item: Flondor Snow White Stand
	<house type="16">
        // 9943.xml  item: Imperial Trade Package  type=4
		<item>
			<id>4077</id>
			<name>Steel</name>
			<icon>00004077.png</icon>
			<desc>Material that has been processed and may be used during crafting. It may also be changed to a different form through alchemy or processing.\n\n- How to Obtain: Use Heating in the Processing window on Melted Iron Shard x5 and Coal x5.</desc>
			<count>5</count>
		</item>
		<item>
            ...
		</item>
        ...
	</house>
    <house>
        ...
    </house>
    ...


    // 5013.xm
    // item: Acacia Sap
    <makelist>
		<item>
			<id>292</id>
			<name>Flare of the Ancients</name>
			<icon>00000292.png</icon>
			<desc>A flare that produces an explosion of brilliant light.\n\n- Stuns nearby enemies for a period of time when used in the Altar of Blood.\n※ Has no effect when used outside of Altar of Blood.\n\n- Cooldown: 2 min\n\n- How to Obtain: Process Dim Origin of Clear Water, Dim Origin of Crimson Flame, Dim Origin of Earth, Ancient Spirit Dust x4 using Simple Alchemy.</desc>
		</item>
        <item>
            ...
        </item>
        ...
	</makelist>


    // 292.xm
    // item: Flare of the Ancients
    <manufacture action="MANUFACTURE_ALCHEMY">
		<item>
			<id>293</id>
			<name>Dim Origin of Clear Water</name>
			<icon>00000293.png</icon>
			<desc>A sphere that contains ancient cool water that is used to make the Flare of the Ancients.\n\n- Usage: Craft Flare of the Ancients\n\n- Crafting Method: Processing ({KeyBind:Manufacture}) - Simple Alchemy\n\n- Crafting Materials: \nDim Origin of Clear Water x1\nDim Origin of Crimson Flame x1\nDim Origin of Earth x1\nAncient Spirit Dust x4\n\n- How to Obtain: Processing ({KeyBind:Manufacture}) - Simple Alchemy with the following materials \nEssence of Nature x2\nPowder of Darkness x10</desc>
			<count>1</count>
		</item>
		<item>
            ...
		</item>
	</manufacture>
    <manufacture action="MANUFACTURE_COOKING">
        ...
	</manufacture>
    ...


    // 729.xml
    // item: Antidote Elixir
	<alchemy>
		<item>
			<id>6355</id>
			<name>Wise Man&apos;s Blood</name>
			<icon>00006355.png</icon>
			<desc>A Processed reagent capable of changing the form of other materials through Alchemy.\n\n- How to Obtain:\n &gt; Craft via an Alchemy Tool in your residence if at least Alchemy Apprentice 1.</desc>
			<count>2</count>
		</item>
		<item>
            ...
		</item>
	</alchemy>
    <alchemy>
        ...
    </alchemy>
    ...


    // 4051.xml
    // item: Melted Iron Shard
    // crafting notes -> Gathering
	<collect>
		<character>
			<name>Andesite</name>
		</character>
	</collect>
	<collect>
        ...
	</collect>
    ...


    // 5013.xml
    // item: Acacia Sap
    // crafting notes -> Node Production
    <node region="Stonetail Wasteland - Lumbering"/>
    ...


    // 9205.xml
    // item: Aloe Cookie
	<cook>
		<item>
			<id>7347</id>
			<name>Aloe</name>
			<icon>00007347.png</icon>
			<desc>Aloe is a specialty of Mediah.\nUsage: Aloe Cookie, Aloe Yogurt, etc.\n- How to Obtain: It can be obtained at Ahto Farm. Mediah Aloe can also be Gathered using Bare Hands or a Hoe.</desc>
			<count>5</count>
		</item>
		<item>
            ...
		</item>
        ...
	</cook>
    <cook>
        ...
    </cook>
    ...



</itemInfo>
```