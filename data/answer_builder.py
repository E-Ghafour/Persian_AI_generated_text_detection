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
    return (system_content_prompt + '\n' + random_exapmle(example_names, example_path))[:3800]

def user_read_prompts(file_path):
    with open(file_path, 'r', encoding='utf8') as ff:
        prompts = ff.readlines()
    return [prompt for prompt in prompts if len(prompt)>3]

def save_answers(answers, target_path):
    data = pd.DataFrame([answer.values() for answer in answers], columns=answers[0].keys())
    data.to_csv(target_path, index=False)

def answer_builder(question_path, start_ind, end_ind, api_key, example_path, category):
    openai.api_key = api_key
    example_names = os.listdir(example_path)
    answers = []

    for number_of_file in tqdm(range(start_ind, end_ind), total=end_ind-start_ind):
        answers = []
        file_name = f'{number_of_file}.txt'
        user_prompts = user_read_prompts(os.path.join(question_path, file_name))
        for number_of_quesion, prompt in tqdm(enumerate(user_prompts), total=len(user_prompts)): 
            try:
                system_prompt = system_prompt_builder(
                    example_names=example_names,
                    example_path=example_path
                )
                response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": prompt},
                            ]
                )
                answer = response.choices[0].message.content

                answers.append({
                    'id': f'{number_of_file}.{number_of_quesion}',
                    'system_prompt': system_prompt,
                    'user_prompt': prompt,
                    'category': category,
                    'answer': answer
                })

            except Exception as e:
                print(f'An error occurred in {number_of_file}.{number_of_quesion}th iteration:', str(e))

        save_answers(answers, f'{number_of_file}.csv')

        if(number_of_file%10 == 0):
            gc.collect()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--question_path', type=str)
    parser.add_argument('--start_ind', type=int, default=0)
    parser.add_argument('--end_ind', type=int, default=71)
    parser.add_argument('--api_ind', type=int)
    parser.add_argument('--example_path', type=str)
    parser.add_argument('--category', type=str)
    args = parser.parse_args()
    question_path = args.question_path
    start_ind = args.start_ind
    end_ind = args.end_ind
    api_ind = args.api_ind
    example_path = args.example_path
    category = args.category
    answer_builder(
        question_path=question_path,
        start_ind=start_ind,
        end_ind=end_ind,
        api_key=api_dict[api_ind],
        example_path=example_path,
        category=category
    )