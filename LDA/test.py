from LDA.lda import *
import gensim

testString = 'I’m so upset!! I don’t even know where to begin!\n\n\nTo start off, I think I completely failed my geometry quiz, which I know I should’ve studied more for...my dad’s not gonna be happy about that. :( Then, we had a pop quiz in history on the reading homework from last night, and I completely forgot most of what I read, which made me even more upset because I actually did the reading! But what really made me mad was the note that Sarah slipped into my locker during passing period. She said she was sad that I’ve been hanging out with Jane more lately and thinks that I don’t want to be her friend anymore. I can’t believe she thinks that, especially after talking with her on the phone for hours and hours last month while she was going through her breakup with Nick! Just because I’ve been hanging out with Jane a little more than usual doesn’t mean I’m not her friend anymore. She completely blew me off at lunch, and when I told Jane, she thought that Sarah was being a “drama queen.”\n\n\nhis is just what I need! My parents are getting on my case about doing more extracurricular activities, I have a huge paper due for AP English soon, and I can’t understand a thing in advanced Spanish! The last thing I need is for my best friend to think I hate her and barely text me back anymore.\n\n\nUggh! I can’t concentrate on anything right now because of it. I hope she gets over it!!!'
print(testString)
#testString = lemmatize_stemming(testString)
#print('\n\n---------------------------------------------------------------------------\n\n')
#print(testString)

sentences = split_into_sentences(testString)
docs = []
for sentence in sentences:
    sentence = pre_process(sentence)
    if len(sentence) != 0:
        docs.append(sentence)
print('\n\n---------------- 1 -----------------------------------------------------------\n\n')
print(docs)
print('\n\n---------------- 2 -----------------------------------------------------------\n\n')

dictionary = gensim.corpora.Dictionary(docs)

print(dictionary)
print('\n\n---------------- 3 -----------------------------------------------------------\n\n')

bow_corpus = [dictionary.doc2bow(doc) for doc in docs]

lda_model =  gensim.models.LdaMulticore(bow_corpus,
                                   num_topics = 8,
                                   id2word = dictionary,
                                   passes = 10,
                                   workers = 2)


#print(lda_model.)