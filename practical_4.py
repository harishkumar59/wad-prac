#pip install pandas scikit-learn
#make sure you have csv file



import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load dataset
spam_df = pd.read_csv('spam_data.csv', encoding='latin-1')

# Display first few rows
print(spam_df.head())

# Split data into input and output
X = spam_df['text']
y = spam_df['label']

# Training and Testing data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Convert text into numerical vectors
vectorizer = CountVectorizer()

X_train_vect = vectorizer.fit_transform(X_train)
X_test_vect = vectorizer.transform(X_test)

# Train model
clf = MultinomialNB()
clf.fit(X_train_vect, y_train)

# Model Accuracy
accuracy = clf.score(X_test_vect, y_test)

print("Accuracy: {:.2f}%".format(accuracy * 100))

# Testing with new message
new_message = [input("Enter your message:\n")]

new_message_vect = vectorizer.transform(new_message)

prediction = clf.predict(new_message_vect)

# Output result
if prediction[0] == "spam":
    print("The message is SPAM")
else:
    print("The message is GENUINE")
