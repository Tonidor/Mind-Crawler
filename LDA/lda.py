import gensim
from nltk.stem import *
import re

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences



def lemmatize_stemming(text):
    stemmer = PorterStemmer()
    #text = str.split(text)
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))



# Tokenize and lemmatize
def pre_process(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))

    return result


def lda_model(docs,numOfTopics):
    processedDocs = []
    for doc in docs:
        doc = lemmatize_stemming(doc)
        doc = pre_process(doc)
        if len(doc) != 0:
            processedDocs.append(doc)


    dictionary = gensim.corpora.Dictionary(processedDocs)
    bow_corpus = [dictionary.doc2bow(doc) for doc in processedDocs]

    ldaModel = gensim.models.LdaMulticore(bow_corpus,
                                               num_topics=numOfTopics,
                                               id2word=dictionary,
                                               passes=10,
                                               workers=2)
    for i in range(0,ldaModel.num_topics):
        print(ldaModel.show_topic(i))
    return ldaModel
# Convert processed data to bag of words

