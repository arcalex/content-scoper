# This Python file uses the following encoding: utf-8
import re

# Spliting by word boundaries
word_bound_regex = re.compile(r"\W+")

arabic_handles = \
    [
        ('ه', ['ة']),\
        ('ي', ['ى']),\
        ('ا', ['أ','إ','آ']),\
        # ('و', ['ؤ']),\
        ('', ['ّ','‘','ٌ','ُ','ً','َ','ِ','ٍ','ـ','’','ْ','~'])
    ]

def read_stop_words():
    stop_words = open('ar_stopwords.txt','r').read().splitlines()
    #unify arabic letters
    for key, arr in arabic_handles:
        for a in arr:
            stop_words = [word.replace(a, key) for word in stop_words] 
    return stop_words


def remove_stop_words(text):
    stop_words = read_stop_words()
    lines = text.splitlines()
    new_lines = []
    for line in lines:
        if line.strip():  #if not empty
            words = line.split()
            for w in range(0, len(words)):
                word = words[w]
                if word in stop_words:
                    words[w] = ""
            line = " ".join(words)
            line = line.replace("  "," ")
            new_lines.append(line)
    return '\n'.join(new_lines)


def regex_union(arr):
    return '(' + '|'.join( arr ) + ')'

#For punctuation replacement
def punctuations_repl(match):
    text = match.group(0)
    repl = []
    for (key, parr) in punctuations :
        for punc in parr :
            if punc in text:
                repl.append(key)
    if( len(repl)>0 ) :
        return ' '+' '.join(repl)+' '
    else :
        return ' '

def processPunctuations( text):
    return re.sub( word_bound_regex , punctuations_repl, text )

def contains_arabic_letters(text):
    arr = re.findall(r'[\u0600-\u06FF]+', text)
    if len(arr)>0:
        return True
    else:
        return False

def adjust_num(text):
    # replace all occurence of numbers with __NUN
    lines = text.splitlines()
    num_lines = []
    for line in lines:
        if line.strip():  #if not empty
            words = line.split()
            for w in range(0, len(words)):
                word = words[w]
        #ب50
                if word.startswith("ب") and word[1:].replace(".", "").replace(",", "").isdigit():
                    words[w] = "ب" + "__NUM"
        #50ج
                elif word.endswith("ج") and word[:-1].replace(".", "").replace(",", "").isdigit():
                    words[w] = "__NUM" + "ج"
                #50
                elif words[w].replace(".", "").replace(",", "").isdigit():
                    words[w] = "__NUM"
            line = " ".join(words)
            num_lines.append(line)
    return '\n'.join(num_lines)

#main function
def normalize(text):

    #handle follows expressions
    text =text.strip().lower()
    #print(text)
    #remove diactrice and unify arabic letters
    for key, arr in arabic_handles:
        for a in arr:
            text = text.replace(a, key)
    #remove stop words
    text = remove_stop_words(text)
    #print(text)
    text = adjust_num(text)
    #handle quotes
    text = text.replace('\'','')
    #handle punctuations
    #text = re.sub( word_bound_regex , punctuations_repl, text )
    
    return text
