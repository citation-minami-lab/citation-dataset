import sys
sys.path.append('../')
from axcell.helpers.datasets import read_arxiv_papers
from pathlib import Path

from pathlib import Path
from axcell.helpers import LatexConverter, Unpack
from axcell.errors import UnpackError, LatexConversionError
from axcell.data.elastic import Paper as PaperText
import axcell.data.extract_tables as table_extraction
import re
import warnings
import glob
from tqdm import tqdm

arxiv_re = re.compile(r"^(?P<arxiv_id>\d{4}\.\d+(v\d+)?)(\..*)?$")


class PaperExtractor:
    def __init__(self, root):
        self.root = Path(root)
        self.unpack = Unpack()
        self.latex = LatexConverter()

    def __call__(self, source):
        source = Path(source)

        m = arxiv_re.match(source.name)
        if not m:
            warnings.warn(f'Unable to infer arxiv_id from "{source.name}" filename')
            arxiv_id = source.name
        else:
            arxiv_id = m.group('arxiv_id')

        subpath = source.relative_to(self.root / 'sources').parent / arxiv_id
        unpack_path = self.root / 'unpacked_sources' / subpath
        try:
            self.unpack(source, unpack_path)
        except UnpackError as e:
            if e.args[0].startswith('The paper has been withdrawn'):
                return 'withdrawn'
            return 'no-tex'
        return 'success'


ROOT_PATH = Path('../../')
SOURCES_PATH = ROOT_PATH / 'sources'
extract = PaperExtractor(ROOT_PATH)

files = SOURCES_PATH.iterdir()
count_success = 0
count_notex = 0
count_error = 0

with open('data_list.txt', mode='w') as f:
    for file in tqdm(files):
        try:
            output = extract(file)
        except:
            output = 'error'
        if output == 'success':
            count_success = count_success + 1
        elif output == 'no-tex':
            count_notex = count_notex + 1
        elif output == 'error':
            count_error = count_error + 1
        f.write(str(file).split('/')[-1] + ',' + output + '\n')
print(count_success, count_notex, count_error)
