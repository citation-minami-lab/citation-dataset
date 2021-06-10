import re
import pathlib

def cite_counter(text):
    citations = re.findall('(?<=cite{).*?(?=})', text)
    cite_count = 0
    for citation in citations:
        cite_count = cite_count + 1
    return cite_count

def tail_check(text):
    with open('tail.txt', 'a') as save_file:
        save_file.write(text[-1])


path_citation_list = '../../ref_analyse/dataset/table.csv'
path_axcell_data = '../../ref_analyse/dataset/axcell_data/'
citation_dict = {}
citation_dict_bfo = {}

'''
with open(path_citation_list) as table:
    lines = table.readlines()
    for line in lines:
        arxiv_id = line.split(' , ')[0]
        citation = line.split(' , ')[1]
        abstract_id = line.split(' , ')[3].replace('\n', '')
        if arxiv_id not in citation_dict:
            citation_dict[arxiv_id] = {}
        citation_dict[arxiv_id][citation] = abstract_id

with open('../../ref_analyse/settings/testdata.csv') as test_path:
    lines = test_path.readlines()
    for line in lines:
        id = line.replace('\n', '')
        citation_dict.pop(id)

'''
with open(path_citation_list) as table:
    lines = table.readlines()
    for line in lines:
        arxiv_id = line.split(' , ')[0]
        citation = line.split(' , ')[1]
        abstract_id = line.split(' , ')[3].replace('\n', '')
        if arxiv_id not in citation_dict_bfo:
            citation_dict_bfo[arxiv_id] = {}
        citation_dict_bfo[arxiv_id][citation] = abstract_id

with open('../../ref_analyse/settings/testdata.csv') as test_path:
    lines = test_path.readlines()
    for line in lines[500:]:
        id = line.replace('\n', '')
        data = citation_dict_bfo.pop(id)
        citation_dict[id] = data
'''

cite_count_list = [0] * 15
for i, arxiv_id in enumerate(citation_dict):
    path_pathlib = pathlib.Path(path_axcell_data + arxiv_id)
    related_works = path_pathlib.glob('*.tex.split')
    for related_work in related_works:
        with open(str(related_work)) as related_work_path:
            texts = related_work_path.readlines()
            for text in texts:
                if cite_counter(text) > 14:
                    cite_count_list[0] = cite_count_list[0] + 1
                else:
                    #print(cite_counter(text), text, arxiv_id)
                    cite_count_list[cite_counter(text)] = cite_count_list[cite_counter(text)] + 1
print(cite_count_list[1], cite_count_list[2], sum(cite_count_list[3:]))
print(len(citation_dict))
