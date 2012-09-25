# -*- coding: utf8 -*-
from pydelicious import get_popular,get_userposts,get_urlposts
import os
from pickle import load,dump
from collections import defaultdict
from time import sleep

def get_similar_users(tag,count = 5):
    return [post_info["user"]
            for url_info in get_popular(tag)[:count]
                for post_info in get_urlposts(url_info["url"])]
def get_prefs(users):
    prefs = defaultdict(dict)
    all_urls = set()
    for user in users:
        #repetive request, iteration out = 3
        print users.index(user)
        for i in xrange(4):
            try:
                posts = get_userposts(user)
                break
            except:
                print "retrying %s" %user
                sleep(3)
                
        for post in posts:
            prefs[user][post["url"]] = 1.
            all_urls.add(post["url"])
    print len(prefs[users[0]])
    for user in users:            
        for url in all_urls:
            if url not in prefs[user]:
                prefs[user][url] = 0.#set unsaved urls' value to 0
    print len(prefs[users[0]]),len(all_urls)
    return prefs

if __name__ == "__main__":
    user_path = "cache/delicious_users"
    if os.path.exists(user_path ):
        users = load(open(user_path,"r"))
    else:    
        print "fetching usernames"
        users = get_similar_users(u"python",count = 5)
        users.append("xiaohan2012")#add myself,hehe!
        dump(users,open(user_path,"w"))

    print "user count: %d" %len(users)
    
    prefs_path = "cache/delicious_prefs"
    if os.path.exists(prefs_path ):
        prefs = load(open(prefs_path ,"r"))
        print len(prefs)
    else:
        print "fetching user post info"
        prefs = get_prefs(users)
        dump(prefs,open(prefs_path ,"w"))
    ratio = [sum(prefs[user].values())/len(prefs[user].values()) for user in prefs]
    ratio.sort(reverse = True)
    
    from recommendations import top_matches,get_recommendations
    import random
    #user = random.choice((prefs.keys()))
    print user
    user = "xiaohan2012"
    print top_matches(user,prefs)
    print get_recommendations(user,prefs)
    print "It is empty, I think we might have encountered data sparsity problem, haha"
