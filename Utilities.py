import csv
import pickle


def save_list_as_csv(mylist:list, fname:str, d=','):
    with open(fname, 'w', newline='') as csvfile:
        sw = csv.writer(csvfile, delimiter=d)
        for row in mylist:
            sw.writerow(row)

def load_p_and_save_csv(mypickle:str, fname:str, d=','):
    with open(mypickle, mode='rb') as f:
        mylist = pickle.load(f)
    save_list_as_csv(mylist, fname, d)

