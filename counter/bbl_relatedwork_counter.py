import pathlib

axcell_src_path = pathlib.Path('../ref_analyse/dataset/axcell_data/')
axcell_folders = axcell_src_path.iterdir()

related_list = []
#related_work存在
for axcell_folder in axcell_folders:
    related_list.append(axcell_folder.name)

count_1 = 0
count_0 = 0
# bbl 存在
with open('save.csv') as load_file:
    lines = load_file
    for line in lines:
        #print(line.replace('\n', ''))
        if line.replace('\n', '') in related_list:
            count_1 = count_1 + 1
        else:
            count_0 = count_0 + 1
print(count_1, count_0)
