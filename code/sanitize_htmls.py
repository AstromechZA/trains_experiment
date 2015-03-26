import os
import re


def collect_htmls(d):
    return map(lambda f: os.path.join(d, f), filter(lambda f: f.endswith('.htm'), os.listdir(d)))


def read_content(p):
    with open(p, 'r') as f:
        return f.read()


def strip_comments(lines):
    return re.sub('<!--[\s\S]*?-->', '', lines)


def convert_filename(filename):
    return filename + '.stripped'


def write_data(filename, lines):
    with open(filename, 'w') as f:
        f.write(lines)


directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(directory, 'data')

filenames = collect_htmls(data_dir)
for f in filenames:
    content = strip_comments(read_content(f))
    write_data(convert_filename(f), content)
