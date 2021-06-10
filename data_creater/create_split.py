import pathlib


def split_tex_text(path):
    path_pathlib = pathlib.Path(path)
    texes = path_pathlib.glob('*.tex')
    is_citation = False
    for tex in texes:
        tex_path = str(tex)
        citation_text = []
        with open(tex_path) as file:
            full_text = ''
            text_list = []
            lines = file.readlines()
            for line in lines:
                if line == '\n':
                    full_text = full_text + '. '
                else:
                    full_text = full_text + line.replace('\n', ' ')
            text_list = full_text.split('. ')
            for text in text_list:
                if '\\cite{' in text:
                    citation_text.append(text)
        save_file_name = tex_path.split('/')[-1] + '.split'
        if citation_text:
            is_citation = True
            with open(path + '/' + save_file_name, 'w') as save_file:
                for text in citation_text:
                    save_file.write(text + '\n')
    return is_citation
