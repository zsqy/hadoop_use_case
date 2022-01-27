#!/usr/bin/python3

from mrjob.job import MRJob
from mrjob.step import MRStep
import mrjob

#class ValueProtocol(object):
#    def write(self, key, values):
#        return ';'.join(str(v) for v in values)

class getresult(MRJob):

    '''
    get final result from the former two steps

    step1 got (MovieID1, MovieID2), (similarity, n)
    step2 got (MovieID1, MovieID2), (MovieName1, MovieName2)

    what we want (MovieName1, MovieName2), (similarity, n)
    '''
#	OUTPUT_PROTOCOL=ValueProtocol
    INPUT_PROTOCOL = mrjob.protocol.JSONProtocol
    PARTITIONER = 'org.apache.hadoop.mapred.lib.HashPartitioner'
    #JOBCONF = {'mapred.map.tasks': 3}
    JOBCONF = {'mapred.reduce.tasks': 3}

    def steps(self):
        return [MRStep(mapper=self.group_by_idpairs, reducer=self.generate_final_result)]

    def group_by_idpairs(self, key, values):
        if len(values) == 2:
            name1, name2 = values
            yield key, list((name1, name2))
        else:
            s1, s2, s3, n = values
            yield key, list((s1, s2, s3, n))

    def generate_final_result(self, key, values):

        f = [1, 2]
        for item in values:
            if len(item) == 2:
                f[0] = item
            if len(item) == 4:
                f[1] = item
            if not isinstance(f[1], int) and not isinstance(f[0], int) and len(f[1]) == 4 and len(f[0]) == 2:
                yield None, f


if __name__ == '__main__':
    getresult.run()
