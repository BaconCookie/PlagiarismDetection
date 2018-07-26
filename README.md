# PlagiarismDetection with a WORD2VEC implementation
An explorative / examplary implementation of a plagiarism detection using the word2vec implementation of spaCy

Author: Laura H.
# Finding Plagiarisms with Word2Vec 

## What is Word2Vec
Word2Vec utilizes vector representations of words, "word embeddings".
Word embedding is a popular framework to represent each word as a vector in
a vector space of many (for example 300) dimensions, based on the semantic
context in which the word is found.[1] This technique has been used in many
machine learning and natural language processing tasks.[2] The term word em-
bedding is being used to describe multiple word vectors in a data set as well as
for a single word vector in such a word embedding.
Imagining such high-dimensional vectors and word embeddings is challeng-
ing. Therefore, a tool - the Embedding Projector[3] - has been developed for
interactive visualization of high-dimensional data by rendering them in two or
three dimensions. The example in Figure 1 is based on input data from Word2Vec
All, which means this word embedding consists of roughly 70.000 vectors with
200 dimensions. Word2Vec[5] is a publicly available trained model and one from
the collection of models in the Embedding Projector by Google. To reduce the
dimensionality of this data set, the t-SNE (T-distributed stochastic neighbor
embedding), a nonlinear nondeterministic algorithm has been chosen because it 
tries to preserve local neighborhoods in the data, meaning that vectors of words
with similar semantics are being projected in close approximation.[4]

![Figure 1 the Embedding Projector ](./images/embeddingprojector.png)

*Figure 1 the Embedding Projector. 
An example of a word embedding visualization after it has been rendered in
two dimensions. Each dot represents a vector of 200 dimensions. Nearest neighbors of
the computer vector in the original space are highlighted in the graph and listed on
the right side.[3]*

## Algorithm Idea
As we can see in Figure 1, words which convey the same meaning / are about the same
subject are clustered together. Words concerning other topics will be further away. 
We can compute how close words represented by a word embedding are to each other, 
by calculating the cosine similarity (direction) of these vectors. 
A cosine similarity of 1 means it is the same word.
A cosine similarity going towards 0 means the words are completely different.

If we do this word by word, we would know how much the separate words are alike.
Yet, plagiarisms are more about sentences and paragraphs rather than words.
Therefore, we should rather calculate the mean vectors of sentences and compare these.
During explorative testing I noticed that a cosine similarity > 0.9 is rather reliable 
indication that sentences are very much alike. Like a plagiarised sentence would be. 
Maybe slightly altered, but in essence the same. 
Therefore, this would be my suggestion to start with if looking for possible plagiarisms.

### Prerequest for WIKIPLAG
1. A table in the Cassandra database with:
* sentenceID
* sentence
* title/ID of article the sentence belongs to

### Algorithm
0. Possibly TF-IDF for speedup
1. Split the text which is to analyse (TextToAnalyse) into sentences 
(for example by using a [Sentence Iterator](https://deeplearning4j.org/sentenceiterator) 
from dl4j).
2. Compare the TextToAnalyse sentences with all the sentences from Wiki (see sentence table as described above)
by using the cosine similarity function 
(see vec.similarity("word1","word2") in [dl4j Word2Vec Tutorial](https://deeplearning4j.org/word2vec.html))
3. If similarity > 0.9 => likely to be a very similar sentence, possible plagiarism.
4. List/Map possible plagiarisms, show to user as possible plagiarisms.

## Implementation
There is no need to implement Word2Vec and the necessary functions from scratch, since 
there are some pretty cool libraries in multiple languages.

As I first had this Idea, I build an explorative implementation in Python using spaCy (that == this project).
I found that the idea worked and that the quality of the Word2Vec models used made quite 
a difference in outcome for, for example, th similarity function. 
I recommend to find the biggest, most diverse model possible an to test with different 
models to see what works best.

For Java/Scala, there is a library deeplearning4j (dl4j) and nd4j 
(dl4j is based on nd4j and there are some functions you might need from here).

WIKIPLAG: I recommend to build this in a separate project (micro service), 
since the dependencies of dl4j and nd4j are not compatible with the current project (sbt). 

## Speeding up the process with TF-IDF
Comparing all sentences from the text to analyse with all sentences in the wiki database requires 
a lot of computing resources. 
Therefore, is seems like an good idea to filter relevant wiki articles first.
We can do that by using [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) 
(term frequency–inverse document frequency).

Begin with calculating the inverse document frequency: how often is a word used in the whole dataset?
I already implemented this in wikiplag-multi/plagFinderWord2Vec and has been calculated for 383 articles.
(For the table with all wikipedia articles (~2 Milion), the spark memory needs to be adjusted or the table 
needs to be read in batches.)

Then, for each new text to analyse, count the frequency of each word in the text to analyse.
The words with are rare in the complete dataset, but are more frequently used in the text to analyse, 
will very likely reveal the subject of the text to analyse. Each word gets a TF-IDF score.

Filter the wiki data for articles about these subjects. 
Pick the top-5 (or any other number that works best.. trail and error here) 
of words with the highest TF-IDF scores, 
and continue with step 1 of the algorithm as described above.

## Literature
  
1. A. Caliskan, J. J. Bryson, and A. Narayanan, “Semantics derived automatically
    from language corpora contain human-like biases,” in Science, vol. 356, pp. 183–186.
2. T. Bolukbasi, K.-W. Chang, J. Y. Zou, V. Saligrama, and A. T. Kalai, “Man is to
    computer programmer as woman is to homemaker? debiasing word embeddings,” in5.
    Advances in Neural Information Processing Systems 29, D. D. Lee, M. Sugiyama,
    U. V. Luxburg, I. Guyon, and R. Garnett, Eds. Curran Associates, Inc., pp.
    4349–4357.
3. Daniel Smilkov, Nikhil Thorat, Charles Nicholson. Embedding projector -
   visualization of high-dimensional data. Online, Available: http://projector.tensorflow.org
4. Google. TensorFlow embeddings. [TensorFlow Embeddings Link](https://www.tensorflow.org/guide/embedding)   
5. T. Mikolov, K. Chen, G. Corrado, and J. Dean, “Efficient estimation of word
    representations in vector space.” Online, Available: http://arxiv.org/abs/1301.3781
