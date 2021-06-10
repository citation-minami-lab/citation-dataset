import xml.etree.ElementTree as ET
import urllib.request as request


def search_title(title, num, save_path):
    url = 'http://export.arxiv.org/api/query?search_query=ti:"' + title.replace(' ', '%20') + '"&start=0&max_results=1'
    req = request.Request(url)
    try:
        with request.urlopen(req) as response:
            XmlData = response.read()
        root = ET.fromstring(XmlData)
    except UnicodeEncodeError:
        return False
    summary = None
    is_exist = False
    file_name = 'arxiv_paper_' + str(num)
    for child1 in root:
        if 'entry' in child1.tag:
            for child2 in child1:
                if 'title' in child2.tag:
                    if title.lower() == child2.text.lower():
                        is_exist = True
                if is_exist == True:
                    if 'summary' in child2.tag:
                        summary = child2.text
                    if 'link' in child2.tag:
                        if child2.attrib['href']:
                            if child2.attrib['href'][-2] == 'v':
                                id = child2.attrib['href']
                                with open(save_path + file_name, 'w') as save_file:
                                    save_file.write(title + '\n' + id + '\n' + summary)
                                return file_name
    return False
