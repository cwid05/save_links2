# This file contains functions that are used to handle the
# urls and query terms

#Need to insert 'libs' into path to use bs4
import sys
sys.path.insert(0, 'libs')

import chris_clean as cc
#import nltk
import string
import urllib



from bs4 import BeautifulSoup
from stop_words import stop_words

table = string.maketrans("","")



def valid_input(term):
    "Neither Urls nor queries (single word) should have spaces"
    return ' ' not in term

def is_url(term):
    """Search terms are all alphanumeric, 
    urls contain some non-alphanumeric character"""
    for char in term:
        if char.isalnum() == False: return True
    return False

def remove_links(string):
    return 'href' not in string
    
def punc(string):
    return string[0].isalnum()

def test_trans(s):
    return s.translate(table, string.punctuation)

def rmv_common(string):
    #stop_words = set(nltk.corpus.stopwords.words('english')) #[]
    #replaced with a python file of the words
    return filter(lambda w: not w in stop_words,string.split())








def crawl_page(url):
    """
    url -> set (unique, uncommon words)
    ...
    Takes a url, gets it's contens, reads 
    all text with in <p> tags and returns a set
    of unique words from this text.
    """
    #Add unique words and remove common words
    try:
        page = urllib.urlopen(url).read()
    except:
        return False
    soup = BeautifulSoup(page)
    words = set()
    for text in soup.find_all('p'):
        clean_text = cc.clean_html(str(text))
        no_punc_txt = test_trans(clean_text)
        lean_clean_text = rmv_common(no_punc_txt)
        for word in lean_clean_text:
            words.add(word.lower())
    return words




# url = 'http://www.udacity.com/cs101x/urank/nickel.html'
# url2 = 'http://www.python.org/dev/peps/pep-0008/'
# result = crawl_page(url2)

# for i in result:
#     print i

# print len(result)



#create crawler to split words from article
# Use beautiful soup to find <p> tags and only crawl those
#    -https://www.udacity.com/course/viewer#!/c-cs101/l-114833207/e-130088232/m-130088231
# split text by spaces
# remove common words
# return list of unique, not-common words

