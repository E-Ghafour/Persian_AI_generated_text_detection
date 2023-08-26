import argparse
import os
from tqdm import tqdm

remove_ = lambda x, char: x[x.index(char)+1:].strip()
fix_bad_lines = lambda lines, char: [remove_(line, char) for line in lines]

def fix_line(lines):
    first_char = lines[0][0]
    socond_char = lines[0][1]
    if(first_char in ['1', '۱', '-']):
        lines = fix_bad_lines(lines, socond_char)
    return lines

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder_path')
    args = parser.parse_args()
    folder_path = args.folder_path
    file_names = os.listdir(folder_path)
    txt_files = [file_name for file_name in file_names if file_name.endswith('.txt')]
    for file_name in tqdm(txt_files):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r', encoding='utf8') as ff:
            lines = ff.readlines()
        lines = fix_line(lines)
        with open(file_path, 'w', encoding='utf8')as ff:
            ff.writelines(line.strip() + '\n' for line in lines)
        