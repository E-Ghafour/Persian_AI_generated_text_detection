import os
from tqdm import tqdm
import openai
import argparse

def extract_topics(topic_path, api_key):

    openai.api_key = api_key
    directory_name = os.path.dirname(topic_path)
    lines = []

    with open(topic_path, 'r', encoding='utf8') as ff:
        for line in ff:
            if(len(line)<5):
                continue
            lines.append(line.strip())

    for i, line in tqdm(enumerate(lines[:70]), total=70):
        try:
            response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                                {"role": "system", "content": 'You will be provided with one topics in Persian and you should give 30 different questions related to that, you must not repeat the exact words which I give you as a topic, you shouldnt give anything but topics, each in separate line.'},
                                {"role": "user", "content": line},
                            ]
                    )
            output = list(response.choices[0].message.content.split('\n'))
            with open(os.path.join(directory_name, f'{i+1}.txt'), 'w', encoding='utf8') as file:
                file.writelines(line.strip() + '\n' for line in output)
        
        except Exception as e:
            print(f'An error occurred in {i+1}th iteration:', str(e))



if __name__ == '__main__':
    api_dict = {1: "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",
                2: "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",
                3: "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",
                4: "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"}
    parser = argparse.ArgumentParser()
    parser.add_argument('--topics', type=str)
    parser.add_argument('--api_id', type=int)
    args = parser.parse_args()
    topic_path = args.topics
    api_id = args.api_id
    print(f'topic_path: {topic_path}\n openai_api: {api_dict[api_id]}')
    extract_topics(topic_path, api_dict[api_id])