"""
by using euclidean distance and Pearson correlation to measure taste similarity,
calculate the top `n` matches of a given person

Note:
metric space material
http://en.wikipedia.org/wiki/Metric_space#Examples_of_metric_spaces
"""
from collections import defaultdict
from numpy import *

#dictionary of movie critics and their ratings of a small
# set of movies
critics={
'Lisa': {'Lady in the Water': 2.5, 
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0, 
        'Superman Returns': 3.5, 
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0},
'Gene': {'Lady in the Water': 3.0, 
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5, 
        'Superman Returns': 5.0, 
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5},
'Michael': {'Lady in the Water': 2.5, 
            'Snakes on a Plane': 3.0,
            'Superman Returns': 3.5, 
            'The Night Listener': 4.0},
'Claudia': {'Snakes on a Plane': 3.5, 
            'Just My Luck': 3.0,
            'The Night Listener': 4.5, 
            'Superman Returns': 4.0,
            'You, Me and Dupree': 2.5},
'Mick': {'Lady in the Water': 3.0, 
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0, 
        'Superman Returns': 3.0, 
        'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0},
'Jack': {'Lady in the Water': 3.0, 
        'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0, 
        'Superman Returns': 5.0, 
        'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,
        'You, Me and Dupree':1.0,
        'Superman Returns':4.0}}

def _to_defaultdict(prefs):
    d_ = defaultdict(lambda :defaultdict(int))
    for name,movies in prefs.items():
        for movie_name,score in movies.items():
            d_[name][movie_name] = score
    return d_            

critics = _to_defaultdict(critics)

def sim_euclidean(prefs,person1,person2):
    """using euclidean distance to measure the similarity between two users' tastes"""
    pp1 = prefs[person1]
    pp2 = prefs[person2]
    movies = set(pp1.keys()).intersection( set(pp2.keys()) )#get the shared movies
    if len(movies) == 0:
        return 0#they are totally different
    score1 = array([pp1[movie] for movie in movies])
    score2 = array([pp2[movie] for movie in movies])
    return 1 / (1 + sum((score2-score1)**2))

def _cov(v1,v2):
    v1 = array(v1);v2=array(v2)
    return mean(v1*v2) - mean(v1)*mean(v2)
def _std_dev(v1):
    return sqrt(mean((v1 - mean(v1))**2))

def sim_pearson(prefs,person1,person2):
    """using pearson correlation to measure the similarity between two users' tastes"""
    pp1 = prefs[person1]
    pp2 = prefs[person2]
    movies = set(pp1.keys()).intersection( set(pp2.keys()) )#get the shared movies
    if len(movies) == 0:
        return 0#they are totally different
    score1 = array([pp1[movie] for movie in movies])
    score2 = array([pp2[movie] for movie in movies])
    return _cov(score1,score2) / ( _std_dev(score1) * _std_dev(score2) )

def top_matches(person , prefs , n=5 , similarity = sim_pearson):
    tastes = [ (similarity(prefs,person,other),other)
                    for other in prefs if person != other]
    tastes.sort(reverse = True)
    return tastes[:n]

def get_recommendations(subject , prefs , similarity = sim_pearson):
    #get items `subject` haven't touched yet
    items1 = set(item for item in prefs[subject] if prefs[subject][item] != 0)
    items2 = set(item for other in prefs if other != subject for item in prefs[other])
    #print items1,items2
    untouched_items = items2- items1
    #print untouched_items
    sims = dict((other,similarity(prefs,subject,other)) 
                    for other in prefs if other != subject)
    #print sims
    like_rank = dict()
    for item in untouched_items:
        score_sum = 0.
        sim_sum = 0.
        for other in sims:
            #ensure `other` has seen the item 
            if prefs[other][item] !=0 and\
                    sims[other] > 0:#ensure the similarity is positive, meaning we are `alike`,at least to some extent
                sim_sum += sims[other]
                score_sum += prefs[other][item] * sims[other]
        #caculating the weighted average                
        if sim_sum != 0.:
            like_rank[item] = score_sum/sim_sum
    
    return sorted(like_rank.iteritems() , key = lambda i:i[1], reverse = True)
    #return sorted(like_rank , key = like_rank.__getitem__ , reverse = True)

def invert_prefs(prefs):
    d_ = defaultdict(lambda :defaultdict(int))
    for person,movies in prefs.items():
        for movie,score in movies.items():
            d_[movie][person] = score
    return d_

if __name__ == "__main__":
    print "measuring similarities between persons"
    print "\nEuclidean similarity between Toby and Jack"
    print sim_euclidean(critics,"Toby","Jack")
    print "\nEuclidean similarity of Lisa herself"
    print sim_euclidean(critics,"Lisa","Lisa")
    print "\nPearson correlation between Lisa and Gene"
    print sim_pearson(critics,"Lisa","Gene")
    print "\nPearson correlation of Lisa herself"
    print sim_pearson(critics,"Lisa","Lisa")
    print "\nTop matches of Toby using Euclidean distance"
    print top_matches("Toby",critics,n=5,similarity = sim_euclidean)
    print "\nTop matches of Toby using Pearson correlation"
    print top_matches("Toby",critics,n=5,similarity = sim_pearson)
    print "\nGet recommendations for Toby"
    print get_recommendations("Toby", critics, similarity = sim_pearson)

    print "#"*20
    print "\nmeasuring similarity between movies(items)"
    print "\nYou can invert the prefs dictionary"
    movies = invert_prefs(critics)
    from pprint import pprint
    pprint(movies["Just My Luck"])
    print "\nEuclidean similarity between Snakes on a Plane and Superman Returns"
    print sim_euclidean(movies,"Snakes on a Plane","Superman Returns")
    print "\nFinding topmatches for Superman Returns using Pearson Correlation"
    print top_matches("Superman Returns",movies , n=5 , similarity = sim_pearson)
    print "\nFinding critics that might feel good about Superman Returns using Pearson Correlation"

    print get_recommendations("Just My Luck",movies)
