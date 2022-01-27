#!/usr/bin/python3

from mrjob.job import MRJob
from mrjob.step import MRStep
from itertools import combinations
import mrjob


class moviename(MRJob):

    OUTPUT_PROTOCOL=mrjob.protocol.JSONProtocol
    PARTITIONER = 'org.apache.hadoop.mapred.lib.HashPartitioner'
    JOBCONF = {'mapred.reduce.tasks': 3}

    def steps(self):
        return [MRStep(mapper=self.group_by_id, reducer=self.generate_all_pairs)]

    def group_by_id(self,key,values):
        itemid,itemname=values.split('|')[0:2]
        yield key,(itemid,itemname)

    def generate_all_pairs(self,key,groups):
        for item1,item2 in combinations(groups,2):
            yield (item1[0],item2[0]),(item1[1],item2[1])


if __name__ == '__main__':
    moviename.run()
