import pathlib
import codecs
import re
import os

#入力　texのパス　保存先のフォルダ
#出力　\citeの中身　related_workの有無
#関連研究の章の抽出と\citeの抽出
def get_relatedwork(path, save_path):
    pattern_start = r'^(?=.*\\section{Related work).*$'
    pattern_work = '(?<=cite{).+?(?=})'
    pattern_end = r'^(?=.*\\section{).*$'
    search_flag = False
    citation_list = []
    context = ''
    try:
        target_tex = codecs.open(path, 'r', 'utf-8', 'ignore')
    except IsADirectoryError:
        #ファイルが存在しない
        print(path)
        return False
    lines = target_tex.readlines()
    for line in lines:
        if search_flag:
            citations_related_work = re.findall(pattern_work, line)
            context = context + line
            if len(citations_related_work) > 0:
                citation_list.append(','.join(citations_related_work))
            # \\section{がきたら終了
            if re.match(pattern_end, line):
                break
        # related_workの発見
        start_order = re.match(pattern_start, line, re.IGNORECASE)
        if start_order:
            context = line + context
            search_flag = True
    target_tex.close()
    if citation_list:
        os.makedirs(save_path, exist_ok=True)
        with open(save_path + '/relatedwork_' + path.name, 'w') as context_file:
            context_file.write(context)
    return citation_list


def load_texs(source_path_pathlib, save_path):
    texes = source_path_pathlib.glob('*.tex')
    citation_list = []
    for tex in texes:
        result = get_relatedwork(tex, save_path)
        if result:
            citation_list.extend(result)
    return citation_list
