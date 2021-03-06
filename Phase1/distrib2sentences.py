# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 14:30:11 2017

@author: thomas
"""

from __future__ import print_function
import re
import operator
import pickle as pk
import numpy as np

def initialize():
    """ Return the list of words, whose indexes are their ID.
    """
    # Read and find couples (word ID, word).
    with open('correspondance.tsv', 'r') as f:
        f = f.read() #f = "Word ID\tWord\n1\tfawn\n2\tlocalizes\n3\tanogeissus"
    matches = re.findall('\n(\d+)\t([\'\w]+)', f)
    
    # Cast ID from string to int.
    for i, couple in enumerate(matches):
        matches[i] = (int(couple[0])-1, couple[1])

    # Sort and return list of words.    
    matches.sort(key=operator.itemgetter(0))
    _, list_words = zip(*matches)
    return list_words

def printt(resultat):
    for word, distance in resultat:
        print('Distance {:.6}: {}'.format(distance, word))

def get_distrib_from_file(filename):
    """ Get the distances of words.
    
    Argument:
        * filename: a path to the filename
    Return:
        * A list of couples like:
         [('yourselves', 0.0007180493557825685),
          ('lavs', 0.0007177011575549841),
          ('progressives', 0.0007173722260631621),
          ('tested', 0.0007169910822995007)]
    """
    with open('scores', 'rb') as f:
        scores = np.abs(pk.load(f))
        scores = scores[0]
        scores = scores.tolist()[0]
        
    list_words_sorted = initialize()
    resultat = zip(list_words_sorted, scores)
    resultat.sort(key=operator.itemgetter(1), reverse=True)
    
    return resultat


def sort_words(path_to_score):
    """ Sort the words and distance in a dictionnary by postag.
    
    All postags are found in a loaded dictionnary. These will be the keys 
    of the returned dictionnary. The value of this dictionnary is a list of
    all couples (word, probability) that belongs to this postag. Then each 
    word from the distribution is compared to the loaded dictionnary, and 
    then added to the right key.
    
    Argument: 
        * A path to the distribution output by TF.
    Returns:
        * The dictionnary postag --> A list of couples (word, proba).
    """
    
    # Load the dictionnary word -> postags
    with open('word_dict_v2', 'rb') as f:
        word_dict = pk.load(f)
    
    # Load the second dictionnary.
    distrib = get_distrib_from_file(path_to_score)
    
    # Add in the third dictionnary the words.
    dic_words = {}
    count_not_found= 0
    for word, proba in distrib:
        if word in word_dict:
            categorie = word_dict[word][0] #Even if several categories are there, I take the first one, arbitrarily.
            if categorie not in dic_words:
                dic_words[categorie] = [(word, proba)]
            else:
                dic_words[categorie].append((word, proba))
        else:
            #TODO: this should not happen because I used the same data for
            # both word_dict and distrib...
            count_not_found += 1
            print("key {} not found in dictionnary.".format(word))
            
    print('{} words not found.'.format(count_not_found))
    
    # Sort every list (the shortest distance is at the end).
    for key, value in dic_words.iteritems():    
        value.sort(key = lambda x:x[1]) 
        print(key, value[0])
    
    return dic_words
    

def final_sentence(s, path_to_scores):

    dic_words = sort_words(path_to_scores)
    
    # Create a dictionnary of the number of the desired words.
    dic_desired = {}
    for postag in s:
        if postag in dic_desired:
            dic_desired[postag] += 1
        else:
            dic_desired[postag] = 1
            
    # Replace the number of the desired words by the desired words themselves.
    for categorie, nb_elements in dic_desired.iteritems():
        dic_desired[categorie] = dic_words[categorie][-1-nb_elements:-1]

    # Create the final string.
    new_s = []
    for postag in s:
        word = dic_desired[postag].pop(-1)[0] # Delete the last (=best) word.
        new_s.append(word)
    new_s = " ".join(new_s)
    
    return new_s

if __name__ == '__main__':
    
    # During this time, the king was a merciful creature.
    # IN, DET, NN, DT, NN, VBD, DT, JJ, NN
    s = ['IN', 'DT', 'NN', 'DT', 'NN', 'VBD', 'DT', 'JJ', 'NN', 'IN', 'DT', 'NN', 'DT', 'NN', 'VBD', 'DT', 'JJ', 'NN', 'IN', 'DT', 'NN', 'DT', 'NN', 'VBD', 'DT', 'JJ', 'NN']
    print(final_sentence(s, 'scores'))












