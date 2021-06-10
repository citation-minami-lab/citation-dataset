import re


def format_title(title_origin):
    em_pattern = r'(?<={\\em ).+?(?=})'
    emph_pattern = r'(?<=\\emph{).+?(?=})'
    remove_list = ['{', '}']
    title_candidate1 = re.findall(em_pattern, title_origin)
    title_candidate2 = re.findall(emph_pattern, title_origin)
    if title_candidate1:
        title = title_candidate1[0]
    elif title_candidate2:
        title = title_candidate2[0]
    else:
        title = title_origin
    for elem in remove_list:
        tmp = title.replace(elem, '')
        title = tmp
    if title[-1] == '.':
        tmp = title[:-1]
        title = tmp
    if r'``' in title:
        if title[:2] == r'``' and title[-3] == ',':
            title = title[2:-3]
    if 'href' in title:
        split_title = title.split(' ')
        start_flag = False
        piece_title = []
        for elem in split_title:
            if start_flag:
                piece_title.append(elem)
            if 'http' in elem:
                start_flag = True
        title = ' '.join(piece_title)
    return title


def pattern1(text_line_list):
    title_pattern = '(?<=newblock )(.*)'
    key_pattern = '(?<={).+?(?=})'
    newblock_list = []
    if len(text_line_list) < 4:
        return False, None, None
    if 'bibitem' not in text_line_list[0]:
        return False, None, None
    for line in text_line_list:
        if 'newblock' in line:
            newblock_list.append(line)
    if not len(newblock_list) == 2:
        return False, None, None
    try:
        key = re.findall(key_pattern, text_line_list[0])[-1]
    except IndexError:
        return False, None, None
    title_candidate = re.search(title_pattern, newblock_list[0])
    if not title_candidate:
        return False, None, None
    title = title_candidate.group()
    return True, title, key


def pattern2(text_line_list):
    key_pattern = '(?<={).+?(?=})'
    title_pattern = '(?<=``).+?(?=,)'
    title = ''
    if len(text_line_list) < 2:
        return False, None, None
    for line in text_line_list[1:]:
        title_list = re.findall(title_pattern, line)
        if len(title_list) > 0:
            title = title_list[0]
            break
    try:
        key = re.findall(key_pattern, text_line_list[0])[-1]
    except IndexError:
        return False, None, None
    if not title:
        return False, None, None
    return True, title, key


def identify_text(text):
    tf, title_origin, key = pattern1(text.split('\n')[1:])
    if not tf:
        tf, title_origin, key = pattern2(text.split('\n')[1:])
    if title_origin:
        title = format_title(title_origin)
    else:
        title = title_origin
    return tf, title, key


def read_bbl(path):
    bbl_dict = {}
    with open(path) as bbl_file:
        # ファイルの読み込み
        try:
            bbl_text = bbl_file.readlines()
        except UnicodeDecodeError:
            return
        # bibitemの検知フラグ
        start_flag = False
        text = ''
        for line in bbl_text:
            if not start_flag:
                # bibitemを発見
                if line.find('bibitem') > 0:
                    start_flag = True
            if start_flag:
                # 改行を外す
                sline = line.strip('\n')
                # sline に文字列があれば整形、なければ save
                if not sline == '':
                    # インデントから始まっていれば接合 カッコの数合わせ
                    if line[0] == ' ':
                        text = text + sline[1:]
                    elif not text.count('{') == text.count('}'):
                        text = text + sline
                    else:
                        text = text + '\n' + sline
                else:
                    tf, title, key = identify_text(text)
                    if tf:
                        bbl_dict[key] = title
                    text = ''
                    start_flag = False
    return bbl_dict


def read_bbls(citation_list, source_path_pathlib):
    result_dict = {}
    bbls = source_path_pathlib.glob('*.bbl')
    bbl_dict = {}
    for bbl in bbls:
        result = read_bbl(str(bbl))
        if result:
            bbl_dict.update(result)
    for citation in citation_list:
        if citation in bbl_dict:
            result_dict[citation] = bbl_dict[citation]
    return result_dict
