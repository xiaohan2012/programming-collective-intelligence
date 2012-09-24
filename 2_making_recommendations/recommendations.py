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
critics={'Lisa': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
'The Night Listener': 3.0},
'Gene': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 3.5},
'Michael': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
'The Night Listener': 4.5, 'Superman Returns': 4.0,
'You, Me and Dupree': 2.5},
'Mick': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 2.0},
'Jack': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

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

def get_recommendations(person , prefs , similarity = sim_pearson):
    #get movies `person` haven't seen
    movies1 = set(movie for movie in prefs[person])
    movies2 = set(movie for other in prefs if other != person for movie in prefs[other])
    unseen_movies = movies2- movies1
    sims = dict((other,similarity(prefs,person,other)) 
                    for other in prefs if other != person)
    print sims
    like_rank = dict()
    for movie in unseen_movies:
        score_sum = 0.
        sim_sum = 0.
        for other in sims:
            #ensure `other` has seen the movie 
            if prefs[other][movie] !=0 and\
                    sims[other] >= 0:#ensure the similarity is positive, meaning we are `alike`,at least to some extent
                sim_sum += sims[other]
                score_sum += prefs[other][movie] * sims[other]
        #caculating the weighted average                
        like_rank[movie] = score_sum/sim_sum
    
    return sorted(like_rank.iteritems() , key = lambda i:i[1], reverse = True)
    #return sorted(like_rank , key = like_rank.__getitem__ , reverse = True)
if __name__ == "__main__":
    #print sim_distance(critics,"Toby","Jack")
    #print sim_distance(critics,"Lisa","Gene")
    #print sim_pearson(critics,"Lisa","Gene")
    #print pearson(critics,"Lisa","Lisa")
    #print top_matches("Toby",critics,n=5,similarity = sim_pearson)
    #print top_matches("Toby",critics,n=5,similarity = sim_euclidean)
    print get_recommendations("Toby", critics, similarity = sim_pearson)
