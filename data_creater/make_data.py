import pathlib
from tqdm import tqdm
import load_tex_src
import load_bbl_src
import create_split
import arxiv_title_request
import time


axcell_src_path = pathlib.Path('../mount/unpacked_sources')
#citation_path = '../table/id_citation_title'
citation_path = '../ex_data/table.csv'
axcell_folders = axcell_src_path.iterdir()
context_related_path = '../dataset/axcell_data/'
arxiv_request_path = '../dataset/arxiv_data/'
# axcell_folderでループ

'''
for axcell_folder in tqdm(axcell_folders):
    #if i > 10:
    #    break
    source_path_pathlib = axcell_folder
    # 抽出したrelatedworkの保存先
    save_path = context_related_path + axcell_folder.name
    # citationIDのリスト (\cite{}の中身)
    citation_list = load_tex_src.load_texs(source_path_pathlib, save_path)
    if citation_list:
        try:
            result_dict = load_bbl_src.read_bbls(citation_list, source_path_pathlib)
        except TypeError:
            print(citation_list)
            break
        #print(axcell_folder.name, result_dict)
        with open(citation_path, 'a') as id_citation_title:
            for citation in result_dict:
                id_citation_title.write(axcell_folder.name + ' , ' + citation + ' , ' + result_dict[citation] + '\n')
'''

'''
context_related_pathlib = pathlib.Path(context_related_path)
related_texs = context_related_pathlib.iterdir()
for child_folder in tqdm(related_texs):
    result = create_split.split_tex_text(context_related_path + child_folder.name)
'''

with open(citation_path) as id_citation_title_path:
    lines = id_citation_title_path.readlines()
    with open('../table/id_citation_title_file', 'a') as id_citation_title_file_path:
        for i, line in enumerate(tqdm(lines[:100])):
            title = line.split(' , ')[2].replace('\n', '')
            file_name = arxiv_title_request.search_title(title, i, arxiv_request_path)
            if file_name:
                id_citation_title_file_path.write(line.replace('\n', '') + ' , ' + file_name + '\n')
            time.sleep(1)
