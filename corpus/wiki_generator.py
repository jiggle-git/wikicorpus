import json
import os
from datetime import datetime

import bz2file
import re

from corpus.wiki_extractor import extract_pages
from wiki_cleaner import clean_content, clean_title


def wiki_process(in_wiki_path, out_jsonl_path, out_error_dir):
    os.makedirs(os.path.dirname(out_jsonl_path), exist_ok=True)
    os.makedirs(out_error_dir, exist_ok=True)

    page_num = 1
    with bz2file.open(in_wiki_path) as wiki_file, open(out_jsonl_path, 'w', encoding='utf-8', newline='') as jsonl_file:
        wiki_pages = extract_pages(wiki_file)
        for d in wiki_pages:
            if not re.findall('^[a-zA-Z]+:', d[0]) and d[0] and not re.findall(u'^#', d[1]):
                print(f'wiki page processing\tcurrent page={page_num}\t{d[2]}:{d[0]}')
                try:
                    cleaned_text = clean_content(d[1])
                    jsonl_file.write(json.dumps({'id': d[2], 'title': clean_title(d[0]), 'content': cleaned_text}, ensure_ascii=False) + '\n')
                except Exception as e:
                    with open(f'{out_error_dir}/{d[0]}_{d[2]}.txt', 'w', encoding='utf-8', newline='') as errorfile:
                        errorfile.write(d[1])
                if page_num % 1000 == 0:
                    jsonl_file.flush()
                page_num += 1


if __name__ == '__main__':
    wiki_process("../zhwiki-latest-pages-articles.xml.bz2", f'../zhwiki-{datetime.now().strftime("%Y%m%d%H%M%S")}.jsonl', '../error_pages')
