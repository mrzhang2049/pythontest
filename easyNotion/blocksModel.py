from typing import List, Union
import json


class Divider:
    def __init__(self, id: str, parent_id: str):
        self.id = id
        self.parent_id = parent_id
        self.text_type = 'divider'

    def __repr__(self):
        return f'分割线:{self.id}'

    @staticmethod
    def get_payload():
        return {
            'type': 'divider',
            'divider': {}
        }


class Image:
    def __init__(self, parent_id: str, url: str):
        self.parent_id = parent_id
        self.text_type = 'image'
        self.url = url

    def get_payload(self):
        return {
            "image": {
                "type": "external",
                "external": {
                    "url": self.url
                }
            }
        }


# github小图类
class Mention:
    def __init__(self, id: str, url: str, parent_id: str):
        self.id = id
        self.url = url
        self.parent_id = parent_id
        self.text_type = 'bulleted_list_item'

    def __repr__(self):
        return f'github小图:{self.url}'

    def get_payload(self):
        return {'bulleted_list_item': {
            'rich_text': [{
                'annotations': {},
                # 'href': self.url,
                'mention': {'link_preview': {'url': self.url},
                            'type': 'link_preview'
                            },
                'plain_text': self.url,
                'text': {'content': ''},
                'type': 'mention'
            }]
        }}


# github大图类
class LinkPreview:
    def __init__(self, id: str, url: str, parent_id: str):
        self.id = id
        self.url = url
        self.parent_id = parent_id
        self.text_type = 'link_preview'

    def get_payload(self):
        return {
            'link_preview': {
                'url': self.url,
            },
            # 'type': 'link_preview'
        }


# 富文本类
class RichText:
    # 初始化函数
    def __init__(self, text_type: str, id: str, parent_id: str, annotations: dict = None, href: str = '',
                 plain_text: str = ''):
        """
        初始化函数
        :param annotations: 富文本配置
        :param href: 超链接
        :param plain_text:文本内容
        :param text_type: 富文本类型
        :param id: 富文本id
        """

        default_annotations = {
            "bold": True,
            "italic": False,
            "strikethrough": False,
            "underline": False,
            "code": False,
            "color": "red"
        }
        self.annotations = annotations if annotations else default_annotations
        self.href = href
        self.plain_text = plain_text if plain_text else ' '
        self.text_type = text_type
        self.id = id
        self.parent_id = parent_id

    # 输出
    def __repr__(self):
        return (self.plain_text if self.plain_text != ' ' else self.text_type) + (self.href if self.href else '')

    def get_payload(self):
        ret = {
            self.text_type: {
                'rich_text': [{
                    'plain_text': self.plain_text,
                    'text': {'content': self.plain_text},
                    'annotations': self.annotations,
                }]  ###只有Callout有
            }
        }
        if self.text_type == "callout":
            ret[self.text_type].update({"icon": {
                "emoji": "⭐"
            },
                "color": "gray_background"
            })
        if self.href:
            ret[self.text_type]['rich_text'][0]['href'] = self.href
            ret[self.text_type]['rich_text'][0]['text']['link'] = {'url': self.href}

        return ret


# 列列表


class TableX:
    def __init__(self, id: str, jsondata: [], parent_id: str, ):
        self.id = id
        self.jsondata = jsondata
        self.text_type = "table"
        self.id = id
        self.parent_id = parent_id

    def get_payload(self):
        table_rows = []
        for item in self.jsondata:
            cells = []
            num_keys = len(item.keys())
            for key, value in item.items():
                if key == "Color":
                    continue
                cells.append(
                    [
                        {
                            "type": "text",
                            "text": {
                                "content": value,
                            },
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": item["Color"] if "Color" in item else "default"
                            },
                            "plain_text": value,
                        }
                    ])

            row = {
                "type": "table_row",
                "table_row": {"cells": cells}
            }
            table_rows.append(row)
        return {
            "type": "table",
            "table": {
                "table_width": num_keys - 1 if "Color" in item else num_keys,
                "has_column_header": False,
                "has_row_header": False,
                "children": table_rows
            }
        }


class TableXArray:
    def __init__(self, id: str, arraydata: [], parent_id: str, ):
        self.id = id
        self.jsondata = arraydata
        self.text_type = "table"
        self.id = id
        self.parent_id = parent_id

    def get_payload(self):
        table_rows = []
        for item in self.jsondata:
            cells = []
            for value in item:
                num_keys = len(item)
                cells.append(
                    [
                        {
                            "type": "text",
                            "text": {
                                "content": value,
                            },
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": 'black' if value > 0 else "default"
                            },
                            "plain_text": value,
                        }
                    ])

            row = {
                "type": "table_row",
                "table_row": {"cells": cells}
            }
            table_rows.append(row)
        return {
            "type": "table",
            "table": {
                "table_width": num_keys - 1 ,
                "has_column_header": False,
                "has_row_header": False,
                "children": table_rows
            }
        }


class Column:
    def __init__(self, id: str, parent_id: str):
        self.id = id
        self.parent_id = parent_id
        self.text_type = 'column'

    @staticmethod
    def get_payload():
        return {
            'type': 'column',
            'column': {}
        }


class ColumnList:
    def __init__(self, id: str, parent_id: str, content: List[Union[Image, TableX]]):
        self.id = id
        self.parent_id = parent_id
        self.text_type = 'column_list'
        self.content = content

    def get_payload(self):
        columns = []
        for i in self.content:
            columns.append({
                "type": "column",
                "column": {
                    "children": [i.get_payload()]}
            })

        ret = {
            "type": "column_list",
            "column_list": {
                "children": columns
            }
        }

        return ret


# 块类
class Block:
    def __init__(self, content: List[Union[Divider, Mention, LinkPreview, RichText, Column, TableX]]):
        """
        初始化函数
        :param content: 富文本对象内容
        """
        self.content = content
        self.parent_id = content[0].parent_id if len(content) else ''

    def __repr__(self):
        return ''.join([str(i) for i in self.content])

    def get_payload(self):
        ret = {}
        for i in self.content:
            ret.update(i.get_payload())
        return ret
# 列
