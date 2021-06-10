from transformers import BertForSequenceClassification
from transformers import BertTokenizer
import torch
import torch.nn as nn
import make_learning_data


id_citation_title_file_path = '../table/id_citation_title_file'
arxiv_data_path = '../dataset/arxiv_data/'
axcell_data_path = '../dataset/axcell_data/'

'''
id_citation_title_file_path = '../../ref_analyse/dataset/table.csv'
arxiv_data_path = '../../ref_analyse/dataset/arxiv_data/'
axcell_data_path = '../../ref_analyse/dataset/axcell_data/'
'''

model_save_path = '../net/bert/'
testdata_list_path = '../ex_data/testdata.csv'
batch_size = 2
learning_rate = 1e-4


class Mymodel(nn.Module):
    def __init__(self):
        super(Mymodel, self).__init__()
        self.bert = BertForSequenceClassification.from_pretrained('bert-base-uncased')

    def forward(self, input_data, label):
        input_ids = input_data['input_ids']
        token_type_ids = input_data['token_type_ids']
        attention_mask = input_data['attention_mask']
        output = self.bert(input_ids=input_ids, token_type_ids=token_type_ids, attention_mask=attention_mask, labels=label)
        return output


tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
net = Mymodel()
net.train()
net.to('cuda')
optimizer = torch.optim.SGD(net.parameters(), learning_rate, weight_decay=5e-4)

citation_dict = make_learning_data.create_citation_dict_learning(id_citation_title_file_path, testdata_list_path)

max_epoch = 100
good_data_count = 0
bad_data_count = 0
for epoch in range(max_epoch):
    good_data_count = 0
    bad_data_count = 0
    total_counter = 0
    total_loss = 0
    counter_intermediate = 0
    loss_intermediate = 0
    batch_input = []
    batch_label = []

    for i, id in enumerate(citation_dict):
        data_count = [good_data_count, bad_data_count]
        dataset, data_count = make_learning_data.make_data_fromID_task1(id, arxiv_data_path, axcell_data_path, citation_dict, data_count)
        good_data_count = data_count[0]
        bad_data_count = data_count[1]
        for data in dataset:
            optimizer.zero_grad()
            batch_input.append(data[0])
            batch_label.append(data[1])
            if len(batch_input) > batch_size:
                encoded_input = tokenizer(batch_input, return_tensors='pt', padding=True, truncation=True).to('cuda')
                encoded_label = torch.tensor(batch_label).unsqueeze(0).to('cuda')
                #print(batch_input)
                #print(batch_label)
                #break
                output = net(encoded_input, encoded_label)
                loss = output.loss
                total_loss = total_loss + loss.tolist()
                total_counter = total_counter + 1
                counter_intermediate = counter_intermediate + 1
                loss_intermediate = loss_intermediate + loss.tolist()
                loss.backward()
                optimizer.step()
                batch_input = []
                batch_label = []
        if i % 100 == 0:
            if counter_intermediate == 0:
                with open(model_save_path + 'result.txt', 'a') as save_file:
                    save_file.write(str(i) + ' , ' + '0' + ' , ' + '0' + '\n')
            else:
                with open(model_save_path + 'result.txt', 'a') as save_file:
                    save_file.write(str(i) + ' , ' + str(total_loss / total_counter) + ' , ' + str(loss_intermediate / counter_intermediate) + ' , ' + str(counter_intermediate) + '\n')
            counter_intermediate = 0
            loss_intermediate = 0
    torch.save(net.state_dict(), model_save_path + 'mymodel' + str(epoch) + '.ckpt')
    with open(model_save_path + 'result_epoch.txt', 'a') as save_file:
        save_file.write(str(epoch) + ' , ' + str(total_loss / total_counter) + '\n')
