#need to pip install easyocr and SpeechRecognition
import moviepy.editor as mp
import speech_recognition as sr

#video uploading
video = mp.VideoFileClip("testvideo.mp4")
audio_file = video.audio
audio_file.write_audiofile("Test_video1.wav")

r = sr.Recognizer()
#uploading video
with sr.AudioFile("Test_video1.wav") as source:
    data = r.record(source)
#speech to text
text = r.recognize_google(data)

#machine learning!!
#dependencies for bot
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer

#reading text from image
import easyocr
reader = easyocr.Reader(['en'])
result = reader.readtext('test2.jpg', detail = 0)
r1 = ' '.join(str(e) for e in result).lower() #turning text into one string for the machine

# Our existing set of positive texts to learn from
# We already "know" that these are positive, so we
# can use them as examples to train the machine.
positive_texts = [
    "we love you",
    "they love us",
    "you are good",
    "he is good",
    "they love mary",
    "I am happy",
    "we are all here for a reason",
    "dream big",
    "live, laugh, love",
    "people are great",
    "today is Friday",
    "dream on",
    "believe in yourself",
    "follow your dreams",
    "living, laughing and loving",
    "we are living and learning together"
]

# Same as above, but possible trigger causing texts.
negative_texts =  [
    "Body Mass Index (BMI) is way above average",
    "My body dysmorphia is so bad today",
    "Bulimia",
    "Anorexia",
    "Orthorexia",
    "What I eat in a day",
    "That actually gives me OCD",
    "You are a psycho",
    "So ugly",
    "Too fat",
    "You are so sensitive",
    "I am binge eating",
    "They went through sexual assault",
    "I feel so objectified",
    "You are failing. You are stupid",
    "All you do is sit around and be lazy",
    "My friends are so annoying",
    "You are an idiot",
    "Self-harm will help me relieve anxiety",
    "Sucide",
    "Commit Suicide"
]

# These are the test texts. We pretend that we
# don't know if these are negative or positive.
# We'll use them to test our model and see how good
# it is after the training.
test_texts = [
    "no literally gives me OCD",
    "You look ugly",
    "they are sooo good",
    "I love us",
    "I am so binge eating today",
    text, #video text
    r1
]

# We combine our known positive and negative texts
# into a combined training set to feed into the classifier
training_texts = negative_texts + positive_texts

# We also prepare an equivalent set of labels, to tell the machine
# that the first five texts are negative and the second ones are positive.
# When we feed these into the classifier, it'll use indices to match up
# the texts, e.g. the first label in the list is "negative", so it'll learn
# to associate the "negative" class with the first text.
training_labels = ["possibly triggering"] * len(negative_texts) + ["positive"] * len(positive_texts)

# Here we set up the vectorizer, the first main component of our machine learning solution.
vectorizer = CountVectorizer()

# This isn't really learning anything difficult yet. We just
# feed the data we have into our vectorizer so it can keep a
# consistent mapping. E.g. it might map "bad" to 0, "love" to 1,
# you to 2, etc.
vectorizer.fit(training_texts)
#print(vectorizer.vocabulary_)

# Now we transform all of our training texts into vector form.
# At this point, each text is represented by a list of numbers,
# showing how often that word occurs in the text.
training_vectors = vectorizer.transform(training_texts)

# We'll do the same to our test texts. Each of these is a list
# of numbers too after this step.
testing_vectors = vectorizer.transform(test_texts)

# Here we create our classifier and train it  by "showing" it the training texts and
# the associated labels. It will iterate over the data a few times,
# trying different rules, until it finds a set of rules that works.
classifier = tree.DecisionTreeClassifier()
classifier.fit(training_vectors, training_labels)

# It's easy to "overfit" -- find a set of rules that works very well
# for the set of data that we show the classifier, but which doesn't
# work very well on other data, even if it's similar. Here we ask
# the computer to guess whether our test texts (which it has never
# seen) are more similar to the positive texts or the negative ones so we can check how well it works.
#print(classifier.predict(testing_vectors))

# Then we export the model to a file so that we can visualise it. You can
# copy the content from `tree.dot` to http://www.webgraphviz.com/ to
# see what the tree looks like
tree.export_graphviz(
    classifier,
    out_file='tree.dot',
    feature_names=vectorizer.get_feature_names_out(),
)

for i in range(len(test_texts)):
	print(f"{test_texts[i]}: {classifier.predict(testing_vectors)[i]}")