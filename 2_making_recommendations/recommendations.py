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

def sim_distance(prefs,person1,person2):
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
    #print "_cov",(v1-mean(v1)) * (v2-mean(v2))
    return mean((v1-mean(v1)) * (v2-mean(v2)))

def _std_dev(v1):
    return sqrt(sum((v1 - mean(v1))**2))

def pearson(prefs,person1,person2):
    """using pearson correlation to measure the similarity between two users' tastes"""
    pp1 = prefs[person1]
    pp2 = prefs[person2]
    movies = set(pp1.keys()).intersection( set(pp2.keys()) )#get the shared movies
    if len(movies) == 0:
        return 0#they are totally different
    score1 = array([pp1[movie] for movie in movies])
    score2 = array([pp2[movie] for movie in movies])
    print score1,score2
    print _cov(score1,score2) , cov(score1,score2)
    return _cov(score1,score2) / ( _std_dev(score1) * _std_dev(score2) )


if __name__ == "__main__":
    #print sim_distance(critics,"Toby","Jack")
    #print sim_distance(critics,"Lisa","Gene")
    print pearson(critics,"Lisa","Gene")
    print pearson(critics,"Lisa","Lisa")

