import sys
import os
sys.path.append('../')
print(sys.path)
from axcell.helpers.datasets import read_arxiv_papers
from pathlib import Path


V1_URL = 'https://github.com/paperswithcode/axcell/releases/download/v1.0/'
ARXIV_PAPERS_URL = V1_URL + 'arxiv-papers.csv.xz'
SEGMENTED_TABLES_URL = V1_URL + 'segmented-tables.json.xz'
PWC_LEADERBOARDS_URL = V1_URL + 'pwc-leaderboards.json.xz'

arxiv_papers = read_arxiv_papers(ARXIV_PAPERS_URL)

print(f'Number of papers:           {len(arxiv_papers):8}')
print(f'└── with LaTeX source:      {(~arxiv_papers.status.isin(["no-tex", "withdrawn"])).sum():8}')
print(f'Number of extracted tables: {arxiv_papers.tables.sum():8}')

def get_eprint_link(paper):
    return f'http://export.arxiv.org/e-print/{paper.arxiv_id}'

links = arxiv_papers.apply(get_eprint_link, axis=1)

DL_PATH = Path('../../')

import urllib.request
from tqdm import tqdm
import os

success = 0
fail = 0

axcell_exist_list = []
with open("../../../../ex_data/axcell_list") as load_file:
    lines = load_file.readlines()
    for line in lines:
        axcell_exist_list.append(line.replace('\n', ''))

start_index = int(input('Input start index (If you want default enter 0) : '))
for link in tqdm(links[start_index:]):
    name = link.split('/')[-1]
    url = "http://export.arxiv.org/e-print/" + name
    save_name = DL_PATH / 'sources' / name
    if os.path.exists(str(save_name)):
        continue
    try:
        if name in axcell_exist_list:
            urllib.request.urlretrieve(url, save_name)
            success = success + 1
    except:
        fail = fail + 1
        continue

print(success, 'is downloaded', fail, 'failed')
