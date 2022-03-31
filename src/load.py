import json 
import re
from html import unescape

LABEL_MAP = [
    #0   1   2   3   4   5   6   7   8   9  10  11   
    [0,  6,  2,  8,  9, 11,  3,  5,  1,  4,  7, 10],    #0
    [1,  7, -1, -1,  9, 11,  4, -1, -1, -1, -1, 10],    #1
    [3, -1,  5, -1,  9, 11, -1, -1,  4, -1, -1, 10],    #2
    [4, -1, -1, -1,  9, 11, -1, -1, -1, -1, -1, 10],    #3
    [0,  6,  2,  8, 10, -1,  3,  5,  1,  4,  7, -1],    #4
    [1,  7, -1, -1, 10, -1,  4, -1, -1, -1, -1, -1],    #5
    [3, -1,  5, -1, 10, -1, -1, -1,  4, -1, -1, -1],    #6
    [4, -1, -1, -1, 10, -1, -1, -1, -1, -1, -1, -1],    #7
]


class Key:
    def __init__(self, value: str, x: float, y: float, h: float, props: dict):
        self.item = value
        self.x = x
        self.y = y
        self.w = props["w"]
        self.w2 = props["w2"]
        self.h = props["h"]
        self.h2 = props["h2"]
        self.p = props["p"]
        self.c = props["c"]
        self.lc = props["t"]
        self.r = props["r"]
        self.rx = props["rx"]
        self.ry = props["ry"]
        label = re.sub(r'<span class=[\"\']cd[\'\"]>([^<]*)</span>', lambda m: m[1], value)
        self._parse_labels(label, props)
        

    def text(self, olditem, align):

        items = ["", "", "", "", "", "", "", "", "", "", "", ""]
        for pos, item in enumerate(olditem):
            items[LABEL_MAP[align][pos]] = item
        
        return items
    
    def colors(self, oldcolor, align):

        colors = oldcolor.split('\n')
        if len(colors) > 1:
            item_color = [None] * 12
            for pos, color in enumerate(colors):
                if color is not None and len(color) > 0:
                    item_color[LABEL_MAP[align][pos]] = color
        else:
            item_color = [colors[0]] * 12

        return item_color

    def fontsize(self, size1, size2, isizes, align, items):
        """Helper to parse font sizes for labels"""
        if items.count("") < 11: sizes = [size1] + [size2] * 11
        else: sizes = [size1] * 12  
        if isizes:
            for pos, size in enumerate(isizes):
                if size == 0:
                    sizes[LABEL_MAP[align][pos]] = size1
                else:
                    sizes[LABEL_MAP[align][pos]] = size
        #print(sizes)
        return sizes

    def _parse_labels(self, label: str, props: dict):
        
        item_texts = self.text(label.split('\n'), props["a"])
        item_color = self.colors(props["t"], props["a"])
        item_sizes = self.fontsize( props["f"] , props["f2"] if "f2" in props else props["f"] , props["fa"] , props["a"], item_texts)
        #print(props["f2"] if "f2" in props else props["f"], label)
        #print([(item_texts[idx],item_color[idx],item_sizes[idx]) for idx in range(12)])
        self.labels = [Label(item_texts[idx], item_color[idx], item_sizes[idx]) for idx in range(12)]

def fix_color(color: str, fallback: str):
    """Fix the given color string"""
    if color is not None and re.fullmatch(r"#[a-fA-F0-9]{3,6}", color):
        return color.upper()

    return fallback.upper()

class Label:
    def __init__(self, text: str, color: str, size: int):
        self.text = re.sub("<br ?/?>", "\n", unescape(text))
        self.color = fix_color(color, "#111111")
        self.size = size

class Keyboard:
    def __init__(self):
        self.backcolor = '#EEEEEE'
        self.name = 'Keyboard'

        self.__keys = []

    def add_Key(self, key: Key):
        self.__keys.append(key)

    @property
    def key_count(self):
        return len(self.__keys)

    def __iter__(self):
        return iter(self.__keys)

def select(obj: dict, keys: list) -> dict:
    """Return a copy of the given dict with only the listed keys"""
    return {k: obj[k] for k in keys if k in obj.keys()}

def load(filepath:str) -> Keyboard:

    layout = json.load(open(filepath))

    keyboard = Keyboard()
    rowData = {}
    y = 0

    for rowNum, row in enumerate(layout):
        
        x = 0
        if type(row) != dict:
            # iterate over keys in row
            for pos, value in enumerate(row):
                # we skip over items that aren't keys (which are strings)
                if type(value) == str:
                    # default props values
                    props = {
                        "p": "",
                        "d": False,
                        "w": 1,
                        "h": 1,
                        "w2": 0,
                        "h2": 0,
                        "r": 0,
                        "rx": 0,
                        "ry": 0,
                        "y": 0,
                        "c": "#cccccc",
                        "t": "#111111",
                        "f": 3,
                        "fa": None,
                        "a": 4,
                        # override defaults with any current row data
                        **rowData
                    }

                    prev = row[pos - 1]
                    if type(prev) == dict:
                        props = {**props, **prev}
                        rowData = {**rowData, **select(prev, ["c", "t", "g", "a", "f", "f2", "p", "r", "rx"])}
                        if "x" in prev:
                            x += prev["x"]
                        if "y" in prev:
                            rowData["yCoord"] = prev["y"]
                            y += prev["y"]
                        if "ry" in prev:
                            rowData["ry"] = prev["ry"]
                            if "y" in prev:
                                y = prev["ry"] + rowData["yCoord"]
                            else:
                                y = prev["ry"]
                        elif ("r" in prev and "yCoord" not in rowData) or "rx" in prev:
                            if "ry" in rowData:
                                y = rowData["ry"]
                            else:
                                rowData["ry"] = 0
                                y = 0
                            if "y" in prev:
                                y += prev["y"]

                    props = {**props, **rowData}
                    key = Key(value,x, y, 2, props)
                    # add the key to the current row
                    keyboard.add_Key(key)
                    x += key.w
            y += 1

        else:
            # if the current item is a dict then add its properties to the keyboard
            if "backcolor" in row:
                keyboard.color = row["backcolor"]
            if "name" in row:
                keyboard.name = row["name"]
    return keyboard