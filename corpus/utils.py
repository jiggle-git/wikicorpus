import csv
import json
import math
import os

import pandas


def filepaths(directory: str):
    return [os.path.join(root, file) for root, dirs, collections in os.walk(directory) for file in collections]


def filename(file_path: str, extension: bool = False) -> str:
    if extension:
        return os.path.basename(file_path)
    else:
        return os.path.splitext(os.path.basename(file_path))[0]


def csv2jsonl(paths: list, jsonl_path: str, q_index: int = 0, a_index: int = 1):
    with open(jsonl_path, 'w', encoding='utf-8', newline='') as outfile:
        for path in paths:
            with open(path, 'r', encoding='utf-8', newline='') as infile:
                lines = csv.reader(infile, quoting=csv.QUOTE_ALL)
                for line in list(lines):
                    if not line[q_index] or not line[a_index]:
                        continue
                    outfile.write(json.dumps({'question': line[q_index], 'answer': line[a_index]}, ensure_ascii=False) + '\n')


def split_array(arr: list, num: int) -> list:
    length = len(arr)
    chunk_size = math.ceil(length / num)
    result = []
    for i in range(0, length, chunk_size):
        result.append(arr[i:i + chunk_size])
    return result


def merge_jsonl(paths: list, jsonl_path: str):
    with open(jsonl_path, 'w', encoding='utf-8', newline='') as outfile:
        for path in paths:
            with open(path, 'r', encoding='utf-8', newline='') as infile:
                for line in infile:
                    outfile.write(line)


def count_jsonl(jsonl_path: str):
    with open(jsonl_path, 'r', encoding='utf-8', newline='') as infile:
        lines = infile.readlines()
        return len(lines)


def jsonl2excel(jsonl_path: str, excel_path: str):
    data = []
    with open(jsonl_path, 'r', encoding='utf-8', newline='') as infile:
        for line in infile:
            data.append(json.loads(line.strip()))
    data_frame = pandas.DataFrame(data)
    data_frame.to_excel(excel_path, index=False)


if __name__ == '__main__':
    pass
    jsonl2excel('../collections/法律问答数据集/01 法律文档法条数据集_AUDAQUE.jsonl',
                '../collections/法律问答数据集/法律文档法条数据集.xlsx')

    # jsonl2excel('../collections/法律问答数据集/02 法律文档问答数据集_AUDAQUE.jsonl',
    #             '../collections/法律问答数据集/法律知识问答数据集.xlsx')

    # jsonl2excel('../collections/医学问答数据集/医学知识问答数据集_AUDAQUE.jsonl',
    #             '../collections/医学问答数据集/医学知识问答数据集.xlsx')

