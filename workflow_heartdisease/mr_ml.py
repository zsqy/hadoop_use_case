#!/usr/bin/python3

import re
import numpy as np
import pandas as pd
import pickle
import sys
from mrjob.job import MRJob
from mrjob.protocol import PickleValueProtocol
from mrjob.step import MRStep
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import svm

class MRML(MRJob):

    OUTPUT_PROTOCOL = PickleValueProtocol

    def __init__(self, *args, **kwargs):
        super(MRML, self).__init__(*args, **kwargs)
        self.count = 0
        self.meanOldPeak = 0
        self.meanTRestBPS = 0
        self.meanThalCH = 0
        self.meanChol = 0

    def steps(self):
        return [
            MRStep(mapper=self.drop),
            MRStep(mapper=self.preprocess, reducer=self.train)
        ]

    def drop(self, key, line):
        if 'mean' in line:
            self.meanOldPeak = 1
            self.meanTRestBPS = 2
            self.meanThalCH = 3
            self.meanChol = 4
        else:
            words = line.split(',')
            # drop 'fbs', 'exang', 'restecg', 'ca', 'thal', 'slope' with null values
            if words[7] != 'null' and words[10] != 'null' and words[8] != 'null' and words[13] != 'null' and words[14] != 'null' and words[12] != 'null':
                yield(words[0], line)

    def preprocess(self, key, line):
        words = line.split(',')

        # impute with mean
        if words[11] == 'null':
            words[11] = str(self.meanOldPeak)
        if words[5] == 'null':
            words[5] = str(self.meanTRestBPS)
        if words[9] == 'null':
            words[9] = str(self.meanThalCH)
        if words[6] == 'null':
            words[6] = str(self.meanChol)

        # sex
        words[2] = '1' if words[2] == 'Male' else '0'

        # cp
        if words[4] == 'typical angina':
            words[4] = '0'
        elif words[4] == 'atypical angina':
            words[4] = '1'
        elif words[4] == 'non-anginal':
            words[4] = '2'
        elif words[4] == 'asymptomatic':
            words[4] = '3'

        # fbs
        words[7] = '1' if words[7] == 'True' else '0'

        # restecg
        if words[8] == 'normal':
            words[8] = '0'
        elif words[8] == 'st-t abnormality':
            words[8] = '1'
        elif words[8] == 'lv hypertrophy':
            words[8] = '2'
                  
        # exang
        words[10] = '1' if words[10] == 'True' else '0'

        # slope
        if words[12] == 'upsloping':
            words[12] = '0'
        elif words[12] == 'flat':
            words[12] = '1'
        elif words[12] == 'downsloping':
            words[12] = '2'

        # thal
        if words[14] == 'normal':
            words[14] = '0'
        elif words[14] == 'fixed defect':
            words[14] = '1'
        elif words[14] == 'reversable defect':
            words[14] = '2'

        # num
        words[15] = '0' if words[15] == '0' else '1'

        # drop 'id' and 'dataset' columns
        yield(1, words[1] + ',' + words[2] + ',' + words[4] + ',' + words[5] + ',' + words[6] + ',' + words[7] + ',' + words[8] + ',' + words[9] + ',' + words[10] + ',' + words[11] + ',' + words[12] + ',' + words[13] + ',' + words[14] + ',' + words[15])
                
    def train(self, key, line):
        a = []
        col_names = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalch', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']
        for l in line:
            a.append(l.split(','))
        df = pd.DataFrame(a, columns=col_names)
        df[col_names] = df[col_names].apply(pd.to_numeric)
        df_train, df_test = train_test_split(df, test_size=0.8)
        y_train = np.array(df_train['target'])
        x_train = np.array(df_train.drop('target', axis=1))
        y_test = np.array(df_test['target'])
        x_test = np.array(df_test.drop('target', axis=1))
        model = svm.SVC(kernel='linear', C=1.0)
        model.fit(x_train, y_train)

        yield None, model


if __name__ == '__main__':
    MRML.run()
