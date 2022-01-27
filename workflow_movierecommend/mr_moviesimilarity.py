#!/usr/bin/python3

import mrjob
import numpy as np
from itertools import combinations
from math import sqrt
from mrjob.job import MRJob
from mrjob.step import MRStep

PRIOR_COUNT = 10
PRIOR_CORRELATION = 0


def EuclideanDistance(size, minussquared):
    return (sqrt(minussquared) / float(size)) if size else 0.0

def jaccard(user_in_common, total_user1, total_user2):
    union = total_user1+total_user2-user_in_common
    return (user_in_common / (float(union))) if union else 0.0

def pearsondistance(mean_dot_product, rate_square1, rate_square2):
    numerator = mean_dot_product
    denominator = rate_square1*rate_square2
    return sqrt((numerator / (float(denominator)))) if denominator else 0.0

def cosine(dot_product,rating_norm_squared,rating2_norm_squared):
    numerator = dot_product
    denominator = rating_norm_squared*rating2_norm_squared
    return (numerator/(float(denominator))) if denominator else 0.0

class moviesimilaritis(MRJob):

    OUTPUT_PROTOCOL = mrjob.protocol.JSONProtocol
    PARTITIONER = 'org.apache.hadoop.mapred.lib.HashPartitioner'
    #JOBCONF = {'mapred.map.tasks': 3}
    JOBCONF = {'mapred.reduce.tasks': 3}

    def steps(self):
        return[
            MRStep(mapper=self.group_by_uid, reducer=self.group_by_userrate),
            MRStep(mapper=self.generate_value_pairs, reducer=self.Cal_similarity)]


    def group_by_uid(self,key,values):

        '''
        emit userID,movieID,rating to reducer
        1, (1,3.4)
        2, (2,5.0)
        3, (1,2.0)
        ...
        '''
        values = values.split(',')
        uid,mid,ratings = values[0],values[1],values[2]
        yield uid,(mid,float(ratings))

    def group_by_userrate(self,uid,values):

        '''
        emit Uid,((itemid,rate,.....))
        1,(2,5,((1,2),(2,3)))      User1 rating 2 movies movie1 and moview2 tolal value of ratings is 5
        '''
        # itemcount = 0
        # itemsum = 0
        f = []
        for itemid,rate in values:
            # itemcount+= 1
            # itemsum+= rate
            f.append((itemid,rate))

        yield uid,f

    def generate_value_pairs(self,uid,values):

        '''
        For each User
        generate all possible combinations
        (Movie1,Movie2) (Rating1,Rating2)
        '''
        groups = values
        
        for item1,item2 in combinations(groups,2):
            yield (item1[0],item2[0]),(item1[1],item2[1])

    def Cal_similarity(self,itemids, ratings):
        '''
        Many pairs of movie and ratings
        For example
        (1,2) (5,0,4.5)
        (2,3) (3.1,3,3)
        (3,4) (2.0,3.0)
        (4,2) (1.0,2.3)
        ...
        '''
        sum_xx,sum_yy,sum_xy,sum_x,sum_y,sumx_y,n = 0.0,0.0,0.0,0.0,0.0,0.0,0
        item_pairs,rate = itemids,ratings
        itemx,itemy = item_pairs
    
        tempx = []
        tempy = []
        for x,y in rate:
            sumx_y += (x-y)*(x-y)
            sum_xx+=x*x
            sum_yy+=y*y
            sum_xy=x*y
            sum_x+=x
            sum_y+=y
            tempx.append(x)
            tempy.append(y)
            n+=1
    
        tempx=np.array(tempx)
        tempy=np.array(tempy)
        tempx-=np.mean(tempx)
        tempy-=np.mean(tempy)
        tempx=tempx*tempx
        tempy=tempy*tempy
        sumx2,sumy2=sum(tempx),sum(tempy)
        temp=0.0
        T=tempx*tempy
        for i in range(len(T)):
            temp+=T[i]
        # corr_sim=correaltion(n,sum_xy,sum_x,sum_y,sum_xx,sum_yy)
    
        # reg_corr_sim=regularized_correlation(n,sum_xy,sum_x,sum_y,sum_xx,sum_yy,PRIOR_COUNT,PRIOR_CORRELATION)
    
        cos_sim=cosine(sum_xy,sqrt(sum_xx),sqrt(sum_yy))
    
        pdis=pearsondistance(temp,sqrt(sumx2),sqrt(sumy2))
    
        # jac=jaccard(count,n,n)
    
        edis=EuclideanDistance(n,sumx_y)
    
        if n>20:
            yield (itemx,itemy),(cos_sim,edis,pdis,n)

if __name__ == '__main__':
    moviesimilaritis.run()
