import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
import glob
import os
import shutil
from copy import deepcopy as dcp

#---------Function Definition ------------#
def drop_tail_elements_from_df(df, tail_size):
    """
    'drop_tail_elemenets_from_df' function removes the last 'tail_size' elements from a dataframe

    :param df: type dataframe, the input dataframe
    :param tail_size: type int, user-defined input size determining the last 'tail_size' which needs to be removed from the input df

    :return: a 'df' dataframe without the tail elements, and a 'tail_df' dataframe which contains only the tail elements
    """

    tail_df = df.tail(tail_size)
    df = df.drop(df.tail(tail_size).index)
    tail_df = tail_df.reset_index(drop = True)

    return df, tail_df


def data_SSSplitting(df, split_size, strata_col):
    """
    'data_SSSplitting' function does the Stratified Sampling based on a feature.

    :param df: type dataframe, the input dataframe
    :param split_size: type float between (0,1), the proportion we want to use for test set
    :param strata_cool: type string, a feature in a dataframe that is used in the Stratified Sampling

    :return: two sets with the type of dataframe
    """
    sss = StratifiedShuffleSplit(n_splits = 1, test_size = split_size, random_state = 42)
    set1 = None
    set2 = None

    for set1_index, set2_index in sss.split(df, df[strata_col]):
        set1 = df.loc[set1_index]
        set2 = df.loc[set2_index]

    set1 = set1.reset_index(drop=True)
    set2 = set2.reset_index(drop=True)

    return set1, set2


def moving_files(dataset, src_folder, dst_folder):
    """
    'moving_files' function moves picures into the appropriate folder based on the 'dataset' dataframe

    :param dataset: type dataframe, the input dataframe
    :param src_folder: type string, source folder from which the user wishes to move pictures
    :param dst_folder: type string, destination folder to which the user wishes to move pictures

    :return: none
    """

    if not os.path.exists(dst_folder):
        os.mkdir(dst_folder)

    dataset['fname'] = dataset['id'].astype(str) + '.png'
    print(len(dataset), 'num of file according to the dataset')

    for file in dataset['fname']:
        file_name = os.path.basename(file)
        try:
            shutil.copy(src_folder + file, dst_folder + file_name)
        except OSError as e:
            continue

def main():
    df = pd.read_csv('./output/memes_prepared.csv')
    df['ym'] = df['id'].str[0:7]

    train_set, validTest_set =  drop_tail_elements_from_df(df, tail_size = 10000)
    valid_set, test_set = data_SSSplitting(validTest_set, split_size = 0.5, strata_col='ym')


    dataset_var = [test_set, valid_set]
    dataset_str = ['test_set', 'valid_set']

    for i in range(len(dataset_var)):
        moving_files(dataset_var[i], src_folder = './output/meme_pics/', dst_folder = './output/' + dataset_str[i] + '/')
        dataset_var[i].drop(columns = ['fname', 'ym'], inplace = True)
        dataset_var[i].to_csv('./output/' + dataset_str[i] + '.csv', index = False)


#----------End of Function Definition-------------#

if __name__ == "__main__":
    main()


