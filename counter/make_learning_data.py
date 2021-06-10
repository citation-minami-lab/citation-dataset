import pathlib
import re


def create_citation_dict_learning(id_citation_title_file_path, testdata_list_path):
    citation_dict = {}
    with open(id_citation_title_file_path) as table:
        lines = table.readlines()
        for line in lines:
            id = line.split(' , ')[0]
            citation = line.split(' , ')[1]
            abstract_name = line.split(' , ')[3].replace('\n', '')
            if id not in citation_dict:
                citation_dict[id] = {}
            citation_dict[id][citation] = abstract_name
    if testdata_list_path:
        with open(testdata_list_path) as test_path:
            lines = test_path.readlines()
            for line in lines:
                id = line.replace('\n', '')
                citation_dict.pop(id)
    return citation_dict


def create_citation_dict_devtest(id_citation_title_file_path, testdata_list_path, devortest):
    citation_dict = {}
    citation_dict_bfo = {}
    with open(id_citation_title_file_path) as table:
        lines = table.readlines()
        for line in lines:
            id = line.split(' , ')[0]
            citation = line.split(' , ')[1]
            abstract_name = line.split(' , ')[3].replace('\n', '')
            if id not in citation_dict_bfo:
                citation_dict_bfo[id] = {}
            citation_dict_bfo[id][citation] = abstract_name
    with open(testdata_list_path) as test_path:
        lines = test_path.readlines()
        target = []
        if devortest == 'dev':
            target = lines[:500]
        elif devortest == 'test':
            target = lines[500:]
        else:
            print('--error--')
        for line in target:
            id = line.replace('\n', '')
            data = citation_dict_bfo.pop(id)
            citation_dict[id] = data
    return citation_dict


def load_arxiv_paper(path):
    with open(path) as abstract_path:
        context = ''
        lines = abstract_path.readlines()
        for line in lines[2:]:
            context = context + line.replace('\n', ' ')
    return context


def make_data_fromID_task1(base_arxiv_id, arxiv_data_path, axcell_data_path, citation_dict, data_count):
    dataset = []
    good = data_count[0]
    bad = data_count[1]
    path_pathlib = pathlib.Path(axcell_data_path + base_arxiv_id)
    splits = path_pathlib.glob('*.tex.split')
    if base_arxiv_id in citation_dict:
        for split in splits:
            with open(str(split)) as split_file_path:
                texts = split_file_path.readlines()
                for text in texts:
                    unused_citation_keys = citation_dict[base_arxiv_id].copy()
                    citation_origin_list = re.findall('cite{.*}', text)
                    for citation_origin in citation_origin_list:
                        tmp = re.findall('(?<=cite{).*?(?=})', citation_origin)[0]
                        citations = tmp.split(',')
                        for citation_space in citations:
                            citation = citation_space.replace(' ', '')
                            if citation in citation_dict[base_arxiv_id]:
                                context = load_arxiv_paper(arxiv_data_path + citation_dict[base_arxiv_id][citation])
                                #encoded_input = tokenizer(text.replace('\n', '') + ' [SEP] ' + context, return_tensors='pt')
                                encoded_input = text.replace('\n', '') + ' [SEP] ' + context
                                #print(text.replace('\n', '') + ' [SEP] ' + context)
                                dataset.append([encoded_input, 1])
                                try:
                                    unused_citation_keys.pop(citation)
                                except:
                                    pass
                                good = good + 1
                    for citation in unused_citation_keys:
                        if good > bad:
                            context = load_arxiv_paper(arxiv_data_path + citation_dict[base_arxiv_id][citation])
                            encoded_input = text.replace('\n', '') + ' [SEP] ' + context
                            dataset.append([encoded_input, 0])
                            bad = bad + 1
    return dataset, [good, bad]


def make_data_fromID_task2(base_arxiv_id, axcell_data_path, citation_dict):
    dataset = []
    path_pathlib = pathlib.Path(axcell_data_path + base_arxiv_id)
    splits = path_pathlib.glob('*.tex.split') #引用部分ごとに区切ったtextファイル群
    if base_arxiv_id in citation_dict: #データとして存在するか確認
        for split in splits: #ファイルごとにループ
            with open(str(split)) as split_file_path:
                texts = split_file_path.readlines() #引用部分ごとの区切り
                for text in texts: #文章のfor文
                    citation_origin_list = re.findall('cite{.*}', text) #citation抽出
                    data = []
                    data.append(text.replace('\n', ''))
                    for citation_origin in citation_origin_list: #citationのループ
                        tmp = re.findall('(?<=cite{).*?(?=})', citation_origin)[0]
                        citations = tmp.split(',') #同時引用を分割
                        for citation_space in citations:
                            citation = citation_space.replace(' ', '') #加工
                            if citation in citation_dict[base_arxiv_id]:
                                data.append(citation)
                    if len(data) > 1:
                        dataset.append(data)
    return dataset


def create_data(base_arxiv_id, arxiv_data_path, citation, text, citation_dict, tokenizer):
    context = load_arxiv_paper(arxiv_data_path + citation_dict[base_arxiv_id][citation])
    input = text.replace('\n', '') + ' [SEP] ' + context
    encoded_input = tokenizer(input, padding=True, truncation=True, return_tensors='pt')
    return encoded_input
