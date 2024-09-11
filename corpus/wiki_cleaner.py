import re

from mwparserfromhell.nodes import *

from opencc import OpenCC

import utils
import mwparserfromhell

openCC = OpenCC('t2s')


def clean_title(wiki_title):
    return openCC.convert(wiki_title)


def clean_content(wiki_text: str) -> str:
    # 繁体转换为简体
    wiki_text = openCC.convert(wiki_text)
    wiki_text = re.sub(r'(\'\'\'|\'\'|\-\{\}\-)', '', wiki_text)

    wiki_code = mwparserfromhell.parse(wiki_text)
    lines = []
    ids = []
    for wiki_node in wiki_code.nodes:
        if isinstance(wiki_node, Template):
            template_name = str(wiki_node.name)
            if template_name == 'lang' and len(wiki_node.params) >= 2:
                lines.append(str(wiki_node.params[1]))
            elif (template_name == 'IPA' or 'lang-' in template_name) and len(wiki_node.params) >= 1:
                lines.append(str(wiki_node.params[0]))
        elif isinstance(wiki_node, Text):
            lines.append(wiki_node.value)
        elif isinstance(wiki_node, Wikilink):
            title = str(wiki_node.title) if wiki_node.title else ''
            if title.startswith('File:') or title.startswith('Category:') or title.startswith('Image:'):
                continue
            lines.append(title)
        elif isinstance(wiki_node, Tag):
            tag_name = str(wiki_node.tag)
            if tag_name == 'table':
                continue
            if wiki_node.wiki_markup is not None:
                lines.append(str(wiki_node.contents))
        elif isinstance(wiki_node, Heading):
            # 编号，从第2级开始
            level_num = wiki_node.level - 1
            if len(ids) < level_num:
                ids += [1] * (level_num - len(ids))
            else:
                ids[level_num - 1] += 1
            ids = ids[:level_num]
            ids_str = '.'.join([str(iid) for iid in ids])
            lines.append(f'{ids_str} {clean_content(str(wiki_node.title).strip())}')
        elif isinstance(wiki_node, ExternalLink):
            if wiki_node.title is not None:
                lines.append(str(wiki_node.title))
        elif isinstance(wiki_node, Comment):
            pass
        elif isinstance(wiki_node, Argument):
            pass
        elif isinstance(wiki_node, HTMLEntity):
            pass

    result = re.sub(r'\n+', '\n', ''.join(lines).strip())
    result = '\n'.join([line.strip() for line in result.split('\n') if len(line.strip()) > 0])
    result = re.sub(r'(（）|\(\))', '', result)
    result = re.sub(r'\-\{zh-hans:(.*?);zh-hant:(.*?);.*?\}\-', r'\1', result)
    return result


if __name__ == '__main__':
    pass
    # filepaths = utils.filepaths('wiki')
    # filepaths = ['wiki/Linux内核_130.txt']
    # for filepath in filepaths:
    #     filename = utils.filename(filepath)
    #     with (open(filepath, 'r', encoding='utf-8') as infile,
    #           open(f'wiki_cleaned/{filename}_cleaned.txt', 'w', encoding='utf-8') as outfile):
    #         content = infile.read()
    #         cleaned_wiki = clean_wiki(content)
    #         outfile.write(cleaned_wiki)
    #         outfile.flush()
