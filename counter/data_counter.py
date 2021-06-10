import make_learning_data

id_citation_title_file_path = '../../ref_analyse/dataset/table.csv'
arxiv_data_path = '../../ref_analyse/dataset/arxiv_data/'
axcell_data_path = '../../ref_analyse/dataset/axcell_data/'
testdata_list_path = '../ex_data/testdata.csv'


def task1_count(citation_dict):
    good_data_count = 0
    bad_data_count = 0
    count = 0
    for i, id in enumerate(citation_dict):
        data_count = [good_data_count, bad_data_count]
        dataset, data_count = make_learning_data.make_data_fromID_task1(id, arxiv_data_path, axcell_data_path, citation_dict, data_count)
        good_data_count = data_count[0]
        bad_data_count = data_count[1]
        for data in dataset:
            count = count + 1
    return [good_data_count, bad_data_count, count]


def list_print(list):
    print('good data = ' + str(list[0]))
    print('bad data = ' + str(list[1]))
    print('total = ' + str(list[2]))


citation_dict_train = make_learning_data.create_citation_dict_learning(id_citation_title_file_path, testdata_list_path)
citation_dict_dev = make_learning_data.create_citation_dict_devtest(id_citation_title_file_path, testdata_list_path, 'dev')
citation_dict_test = make_learning_data.create_citation_dict_devtest(id_citation_title_file_path, testdata_list_path, 'test')

print('\n task1_data')
print('--- train data ---')
train_list = task1_count(citation_dict_train)
list_print(train_list)
print('------------------')
print('---- dev data ----')
dev_list = task1_count(citation_dict_dev)
list_print(dev_list)
print('------------------')
print('---- test data ---')
test_list = task1_count(citation_dict_test)
list_print(test_list)
print('------------------ \n')

print('\n task2_data')
data_count = 0
for i, id in enumerate(citation_dict_test):
    dataset = make_learning_data.make_data_fromID_task2(id, axcell_data_path, citation_dict_test)
    for data in dataset:
        labels = []
        text = data[0]
        max_citation = None
        max_acc = 0
        for citation in data[1:]:
            labels.append(citation)
        if len(citation_dict_test[id]) - len(labels) < 2:
            continue
        if len(labels) > 1:
            continue
        data_count = data_count + 1
print('------------------')
print('data count = ' + str(data_count))
print('------------------ \n')
