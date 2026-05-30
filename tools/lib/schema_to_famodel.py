# coding=utf-8
"""
命令行工具：将sqlacodegen生成的ORM定义转换成FastAPI的BaseModel定义
wangkai 22-11-13
"""
import os
import sys
import re
from typing import List
import argparse

def split_by_head(astr: str, areg: str) -> List[str]:
    parts = complete_split(astr, areg)
    rt_list = []
    for i in range( (len(parts) - 1) // 2 ):
        cur = i*2 + 1
        part_str = parts[cur] + parts[cur+1]
        rt_list.append(part_str)
    return rt_list

def split_by_match(a_str: str, match_list: List[str]) -> List[str]:
    split_list = []
    left_str = a_str

    for item in match_list:
        index = left_str.index(item)
        split_str = left_str[0:index]
        split_list.append(split_str)
        left_str = left_str[index + len(item):]  # 迭代子要循环底执行。

    split_list.append(left_str)
    return split_list

def complete_split(astr: str, areg: str) -> List[str]:
    final_list = []
    match_list = re.findall(areg, astr, flags=re.DOTALL) 
    split_list = split_by_match(astr, match_list)

    for i in range(len(match_list)):
        final_list.append(split_list[i])
        final_list.append(match_list[i])

    final_list.append(split_list[-1])

    return final_list

def main():
    parser = argparse.ArgumentParser(description='将sqlacodegen生成的ORM定义转换成FastAPI的BaseModel定义')
    parser.add_argument('--input', type=str)
    parser.add_argument('--output', type=str)
    args = parser.parse_args()
    input_path = args.input
    output_path = args.output
    fstr = open(input_path, "rb").read().decode("u8", "replace")
    fw = open(output_path, "wb")

    fw.write(b"from pydantic import BaseModel\n")
    fw.write(b"from typing import Optional\n")
    parts = split_by_head(fstr, "\nclass \w+")
    for part in parts:
        lines = part.strip().split("\n")
        class_line = lines[0].replace("class T", "class ").replace('(Base)', '(BaseModel)')
        fw.write(class_line.encode('u8') + b"\n")
        lines.pop(0)
        for line in lines:
            if '__table' in line:
                continue
            cols = line.split(" = ")
            if len(cols) != 2:
                continue
            key = cols[0].strip()
            if (
                "String" in cols[1]
                or "TIMESTAMP" in cols[1]
            ):
                val = 'str'
            elif (
                "Integer" in cols[1]
            ):
                val = 'int'
            elif (
                "Float" in cols[1]
            ):
                val = 'float'
            else:
                assert False
            if key != 'id':
                line = "    %s: %s" % (key, val)
            else:
                line = "    %s: Optional[%s]" % (key, val)
            fw.write(line.encode('u8') + b"\n")
    fw.close()

if __name__ == "__main__":
    main()
