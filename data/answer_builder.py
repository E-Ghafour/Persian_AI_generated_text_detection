import os
from tqdm import tqdm
import openai
import argparse
from line_fixer import *
from api_dict import api_dict
import random
import gc

system_content_prompt = """You will be provided with a question and you have to write a persian passage randomly in persian from 1 to 4 paragraphs, the passage is going to be published in a news website and it's the comment or the idea of a second person about a specific subject or a report, you are given an example:"""


def random_exapmle(file_names, dir_path):
    index = random.randint(0, len(file_names))
    file_path = os.path.join(dir_path, file_names[index])
    with open(file_path, 'r', encoding='utf8') as ff:
        exapmle = ff.read()
    return exapmle

def prompt_builder(file_names, example_path):
    return system_content_prompt + '\n' + random_exapmle(file_names, example_path)
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder_path', type=str)
    parser.add_argument('--start_id', type=int, default=0)
    parser.add_argument('--end_id', type=int, default=71)
    parser.add_argument('--api_key', type=int)
    parser.add_argument('--example_path', type=str)
    args = parser.parse_args()
    folder_path = args.folder_path
    start_id = args.start_id
    end_id = args.end_id
    api_key = args.api_key
    example_path = args.example_path
    print(folder_path, start_id, end_id, api_dict[api_key], sep='\n')

