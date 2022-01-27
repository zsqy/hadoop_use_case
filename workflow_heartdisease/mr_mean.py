#!/usr/bin/python3

from mrjob.job import MRJob
from mrjob.step import MRStep
import re

class MRMean(MRJob):

    def __init__(self, *args, **kwargs):
        super(MRMean, self).__init__(*args, **kwargs)
        self.count = 0
        self.sumOldPeak = 0
        self.sumTRestBPS = 0
        self.sumThalCH = 0
        self.sumChol = 0

    def steps(self):
        return [
            MRStep(
                mapper=self.map,
                mapper_final=self.map_final,
                reducer=self.reduce
            )
        ]

    def map(self, key, line):
        words = line.split(',')
        if words[11] != 'null' and words[5] != 'null' and words[9] != 'null' and words[6] != 'null':
            self.count += 1
            self.sumOldPeak += float(words[11])
            self.sumTRestBPS += float(words[5])
            self.sumThalCH += float(words[9])
            self.sumChol += float(words[6])

    def map_final(self):
        yield(1, [self.count, self.sumOldPeak, self.sumTRestBPS, self.sumThalCH, self.sumChol])
        
    def reduce(self, key, packedValues):
        count, oldPeak, trestBPS, thalCH, chol = 0, 0, 0, 0, 0
        for values in packedValues:
            count += float(values[0]) 
            oldPeak += float(values[1])
            trestBPS += float(values[2])
            thalCH += float(values[3])
            chol += float(values[4])
        #yield(1, 1)
        yield('mean', [oldPeak / count, trestBPS / count, thalCH / count, chol / count])



if __name__ == '__main__':
    MRMean.run()
