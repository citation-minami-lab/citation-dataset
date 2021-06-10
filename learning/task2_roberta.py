from transformers import RobertaForSequenceClassification
from transformers import RobertaTokenizer
import torch
import torch.nn as nn
import make_learning_data
from tqdm import tqdm


id_citation_title_file_path = '../table/id_citation_title_file'
arxiv_data_path = '../dataset/arxiv_data/'
axcell_data_path = '../dataset/axcell_data/'
model_save_path = '../net/roberta/'

'''
id_citation_title_file_path = '../../ref_analyse/dataset/table.csv'
arxiv_data_path = '../../ref_analyse/dataset/arxiv_data/'
axcell_data_path = '../../ref_analyse/dataset/axcell_data/'
model_save_path = '../net/roberta/'
'''
testdata_list_path = '../ex_data/testdata.csv'


class Mymodel(nn.Module):
    def __init__(self):
        super(Mymodel, self).__init__()
        self.roberta = RobertaForSequenceClassification.from_pretrained('roberta-base')
        self.softmax = torch.nn.Softmax()

    def forward(self, input_data, label):
        input_ids = input_data['input_ids']
        attention_mask = input_data['attention_mask']
        output = self.roberta(input_ids=input_ids, attention_mask=attention_mask, labels=label)
        return output


def comp_data(output):
    result = softmax(output[1]).tolist()[0]
    if result[1] > result[0]:
        return 1
    else:
        return 0


tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
net = Mymodel()
net.eval()
net.to('cuda')
model_epoch = input('Input epoch count : ')
net.load_state_dict(torch.load(model_save_path + 'mymodel' + model_epoch + '.ckpt'))
softmax = torch.nn.Softmax()
citation_dict = make_learning_data.create_citation_dict_devtest(id_citation_title_file_path, testdata_list_path, 'test')
good = 0
count = 0

for i, id in enumerate(tqdm(citation_dict)):
    dataset = make_learning_data.make_data_fromID_task2(id, axcell_data_path, citation_dict)
    for data in dataset:
        labels = []
        text = data[0]
        max_citation = None
        max_acc = 0
        for citation in data[1:]:
            labels.append(citation)
        if len(citation_dict[id]) - len(labels) < 2:
            continue
        if len(labels) > 1:
            continue
        for citation in citation_dict[id]:
            input_data = make_learning_data.create_data(id, arxiv_data_path, citation, text, citation_dict, tokenizer)
            label = torch.tensor(1).unsqueeze(0).to('cuda')
            result = net(input_data.to('cuda'), label)
            acc = softmax(result.logits)[0][1].tolist()
            if acc > max_acc:
                max_acc = acc
                max_citation = citation
        if max_citation in labels:
            good = good + 1
        count = count + 1
print('Accuracy = ' + str(good / count))
print('Used data count = ' + str(count))
