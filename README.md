# Citation Dataset

## Preparation
#### Environment
* conda 4.8.3

#### Procedure
0. Run the Makefile
  ```
   make
  ```
1. Copy AxCell to dataset/axcell_downloader
  ```
  cd dataset/axcell_downloader
  git clone https://github.com/paperswithcode/axcell
  ```
2. Build the environment with the following command
  ```
  # File under axcell
  conda env create -f environment.yml
  ```
3. Place dlaxcell.py and extract.py in
 dataset/axcell_downloader/axcell/notebooks/

 ```
  mv dlaxcell.py dataset/axcell_downloader/axcell/notebooks/
  mv extract.py dataset/axcell_downloader/axcell/notebooks/
 ```

 and run
 ```
   python dlaxcell.py
   python extract.py
 ```

When the download is interrupted, run dlaxcell.py, enter the index number of the paper used as the starting point of the download (input the value by adding 1 to the highest index number of the downloaded papers).

## Experiment
#### Environment
We tested our programs under the following environment.
* python3.6
* Quadro RTX 8000
* Ubuntu 18.04.5 LTS

#### Requirement
* tqdm
* transformers
* torch
* torchvision

#### Procedure
The experimental procedure should be carried out as follows.
Run the following commands that apply the model under evaluation, which depends on the experiment settings. Replace “(model name)” with the actual model name appearing in the file name.

0. Run data_creater/make_data.py (run only the first time, the behavior is as follows)
    ```
    python data_creater/make_data.py
    ```
    * Extract RelatedWork section
      * (by default, the data is stored in dataset/axcell_data/)
    * Make a request to the arXiv API to retrieve the cited papers
      * (by default, the data is stored in dataset/arxiv_data/)
    * After execution, the number of data created can be viewed in counter/data_counter.py
1. Run learning/(model name)_learning
    ```
    python learning/bert_base_learning.py
    python learning/xlnet_base_learning.py
    ```
    * Models are stored in net/(model name)
    * Loss is output to net/(model name)/result_epoch.txt
    * Batch size is already defined on line 20
2. Run /learning/task1_(model name)
    ```
    python learning/task1_bert.py
    python learning/task1_xlnet.py
    ```
    * When the message "Input 'dev' or 'test'" is displayed, enter one of them.
    * When the message "Input epoch count" is displayed, enter the number of epochs for the model
3. Run learning/task2_(model name)
    ```
    python learning/task2_bert.py
    python learning/task2_xlnet.py
    ```
    * When the message "Input epoch count" is displayed, enter the number of epochs for the model used in the experiment

## How to cite

Please cite the following, if you use this dataset.
```
@inproceedings{narimatsu2021task,
  title={Task Definition and Integration For Scientific-Document Writing Support},
  author={Narimatsu, Hiromi and Koyama, Kohei and Dohsaka, Kohji and Higashinaka, Ryuichiro and Minami, Yasuhiro and Taira, Hirotoshi},
  booktitle={Proceedings of the Second Workshop on Scholarly Document Processing},
  pages={18--26},
  year={2021}
}
```
