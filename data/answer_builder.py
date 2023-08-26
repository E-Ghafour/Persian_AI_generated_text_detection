import os
from tqdm import tqdm
import openai
import argparse
from line_fixer import *
from api_dict import api_dict
import random
import pandas as pd
import gc

system_content_prompt = """You will be provided with a question and you have to write a persian passage randomly in persian from 1 to 5 paragraphs, the passage is going to be published in a news website and it's the comment or the idea of a second person about a specific subject or a report, you are given an example:"""

def random_exapmle(example_names, dir_path):
    index = random.randint(0, len(example_names))
    file_path = os.path.join(dir_path, example_names[index])
    with open(file_path, 'r', encoding='utf8') as ff:
        exapmle = ff.read()
    return exapmle

def system_prompt_builder(example_names, example_path):
    return system_content_prompt + '\n' + random_exapmle(example_names, example_path)

def user_read_prompts(file_path):
    with open(file_path, 'r', encoding='utf8') as ff:
        prompts = ff.readlines()
    return prompts

def save_answers(answers, target_path):
    data = pd.DataFrame([answer.values() for answer in answers], columns=answers[0].keys())
    data.to_csv(target_path)

def answer_builder(folder_path, start_ind, end_ind, api_key, example_path, category):
    openai.api_key = api_key
    example_names = os.listdir(example_path)
    answers = []

    for i in tqdm(range(start_ind, end_ind), total=end_ind-start_ind):
        answers = []
        file_name = f'{i}.txt'
        user_prompts = user_read_prompts(os.path.join(folder_path, file_name))
        for prompt in user_prompts:
            try:
                system_prompt = system_prompt_builder(system_prompt_builder(
                    example_names=example_names,
                    example_path=example_path
                ))
                response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": prompt},
                            ]
                )
                answer = list(response.choices[0].message.content)
                answers.append({
                    'id': i,
                    'system_prompt': system_prompt,
                    'user_prompt': user_prompts,
                    'category': category,
                    'answer': answer
                })

            except Exception as e:
                print(f'An error occurred in {i+1}th iteration:', str(e))
        save_answers(answers)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder_path', type=str)
    parser.add_argument('--start_ind', type=int, default=0)
    parser.add_argument('--end_ind', type=int, default=71)
    parser.add_argument('--api_ind', type=int)
    parser.add_argument('--example_path', type=str)
    parser.add_argument('--category', type=str)
    args = parser.parse_args()
    folder_path = args.folder_path
    start_ind = args.start_id
    end_ind = args.end_id
    api_key = args.api_key
    example_path = args.example_path
    category = args.category
    print(folder_path, start_ind, end_ind, api_dict[api_key], sep='\n')

