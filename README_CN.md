** [ENGLISH](README.md) | [中文](README_CN.md) | **
# BDO Item Data Extractor
这个项目可以提取出黑沙客户端的游戏物品数据。
<span style="color: red">只在美服客户端测试过。其他服的客户端应该也可以</span>

## 提前准备的
* PAZ-Unpacker
* Python (当前使用版本: 3.12.3)

## 使用
<span style="color:red; background-color: yellow;font-weight: bold;font-size: 1.5rem">使用之前你需要知道</span>
> PAZ位置:
```
官网下的客户端:
    Pearlabyss\BlackDesert\Paz

Steam:
    Steam\steamapps\common\BlackDesert\Paz
```
<span style="color:red; background-color: #87CEFA;font-weight: bold;font-size: 1.5rem">物品数据在PAZ-Unpacker中的位置</span>
> 物品位置:
```
ui_data\ui_html\xml
```

> 图标位置:
```
ui_texture\icon\new_icon
ui_texture\icon\new_icon\product_icon_png
```
1. 下载 PAZ-Unpacker，python,
2. 打开PAZ-Unpacker选择PAZ所在的位置（建议先copy一份出来以免游戏数据损坏）
3. 找到位置后直接export
4. 在cmd中打开这个项目
```
打开 main.py，填写导出来的路径和保存路径
# data_path = r'E:\paz_extract\ui_data\ui_html\xml\en'
# save_path = r'E:\paz_extract\ui_data\ui_html\xml\en'
data_path = r''
save_path = r''

下面这个是因为 NA 的英文游戏数据是没有用_en_来做游戏文件的前缀，所以需要指定，如果 TW 的客户端的数据不是_tw_292.xml这样，而是292.xml则需要指定
default_server = ''


----------------------
cmd中输入(项目根目录)：
python -m venv .venv

.\.venv\Scripts\activate

pip install pydantic

python main.py
```


## 结果的文件结构

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

# xml标签与类别对照表 （utils.py的分类方法中参考了这个）
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


## xml中各类数据的标签
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