from transformers import XLNetForSequenceClassification
from transformers import XLNetTokenizer
import torch
import torch.nn as nn
import make_learning_data
from tqdm import tqdm


id_citation_title_file_path = '../table/id_citation_title_file'
arxiv_data_path = '../dataset/arxiv_data/'
axcell_data_path = '../dataset/axcell_data/'
model_save_path = '../net/xlnet/'

'''
id_citation_title_file_path = '../../ref_analyse/dataset/table.csv'
arxiv_data_path = '../../ref_analyse/dataset/arxiv_data/'
axcell_data_path = '../../ref_analyse/dataset/axcell_data/'
model_save_path = '../net/xlnet/'
'''
testdata_list_path = '../ex_data/testdata.csv'


class Mymodel(nn.Module):
    def __init__(self):
        super(Mymodel, self).__init__()
        self.xlnet = XLNetForSequenceClassification.from_pretrained('xlnet-base-cased')
        self.softmax = torch.nn.Softmax()

    def forward(self, input_data, label):
        input_ids = input_data['input_ids']
        token_type_ids = input_data['token_type_ids']
        attention_mask = input_data['attention_mask']
        output = self.xlnet(input_ids=input_ids, token_type_ids=token_type_ids, attention_mask=attention_mask, labels=label)
        return output


def comp_data(output):
    result = softmax(output[1]).tolist()[0]
    if result[1] > result[0]:
        return 1
    else:
        return 0


tokenizer = XLNetTokenizer.from_pretrained('xlnet-base-cased')
devortest = input('Input "dev" or "test" : ')
citation_dict = make_learning_data.create_citation_dict_devtest(id_citation_title_file_path, testdata_list_path, devortest)
net = Mymodel()
net.eval()
net.to('cuda')
softmax = torch.nn.Softmax()
count = 0
count_TP = 0
count_TN = 0
count_FN = 0
count_FP = 0
out = 0
model_epoch = input('Input epoch count : ')
net.load_state_dict(torch.load(model_save_path + 'mymodel' + model_epoch + '.ckpt'))
net.eval()
good_data_count = 0
bad_data_count = 0
for i, id in enumerate(tqdm(citation_dict)):
    data_count = [good_data_count, bad_data_count]
    dataset, data_count = make_learning_data.make_data_fromID_task1(id, arxiv_data_path, axcell_data_path, citation_dict, data_count)
    good_data_count = data_count[0]
    bad_data_count = data_count[1]
    for data in dataset:
        label = data[1]
        encoded_input = tokenizer(data[0], return_tensors='pt', padding=True, truncation=True).to('cuda')
        encoded_label = torch.tensor(data[1]).unsqueeze(0).to('cuda')
        output = net(encoded_input, encoded_label)
        comp = comp_data(output)
        count = count + 1
        if label == comp == 1:
            count_TP = count_TP + 1
        elif label == comp == 0:
            count_TN = count_TN + 1
        elif comp == 1 and label == 0:
            count_FP = count_FP + 1
        elif comp == 0 and label == 1:
            count_FN = count_FN + 1
accuracy = (count_TN + count_TP) / (count_TN + count_TP + count_FN + count_FP)
precision = count_TP / (count_TP + count_FP)
recall = count_TP / (count_TP + count_FN)
fmeasure = (2 * precision * recall) / (recall + precision)
print('accuracy = ' + str(accuracy))
print('precision = ' + str(precision))
print('recall = ' + str(recall))
print('fmeasure = ' + str(fmeasure))
