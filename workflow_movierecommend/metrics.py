from math import sqrt


# def correaltion(size,dot_product,rating_sum,
# 	rating2sum,rating_norm_squared,rating2_norm_squared):
	
# 	numerator=size*dot_product-rating_sum*rating2sum
# 	denominator=sqrt(size*rating_norm_squared-rating_sum*rating_sum)*sqrt(size*rating2_norm_squared-rating2sum*rating2sum)

# 	return (numerator/(float(denominator))) if denominator else 0.0


def EuclideanDistance(size,minussquared):

	return (sqrt(minussquared)/float(size)) if size else 0.0

def jaccard(user_in_common,total_user1,total_user2):
	union=total_user1+total_user2-user_in_common
	return (user_in_common/(float(union))) if union else 0.0

def pearsondistance(mean_dot_product,rate_square1,rate_square2):
	numerator=mean_dot_product
	denominator=rate_square1*rate_square2
	return (numerator/(float(denominator))) if denominator else 0.0
	
def cosine(dot_product,rating_norm_squared,rating2_norm_squared):
	numerator=dot_product
	denominator=rating_norm_squared*rating2_norm_squared
	return (numerator/(float(denominator))) if denominator else 0.0

# def normalized_correlation(size,dot_product,rating_sum,
# 	rating2sum,rating_norm_squared,rating2_norm_squared):

# 	similarity=correaltion(size, dot_product, rating_sum, rating2sum, rating_norm_squared, rating2_norm_squared)
# 	return (similarity+1.0)/2.0

# def regularized_correlation(size,dot_product,rating_sum,
# 	rating2sum,rating_norm_squared,rating2_norm_squared,virtual_cont,prior_correlation):
	
# 	unregularizedCorrelation=correaltion(size, dot_product, rating_sum, rating2sum, rating_norm_squared, rating2_norm_squared)

# 	w=size/float(size+virtual_cont)
# 	return w*unregularizedCorrelation+(1.0-w)*prior_correlation


