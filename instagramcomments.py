import instaloader
import pandas as pd
import nltk
from textblob import TextBlob
import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt

spc = spacy.load("en_core_web_sm")

loader = instaloader.Instaloader()
loader.context.login('Username', 'Password') #<--- Replace Username & Password with your account

url = 'https://www.instagram.com/p/XXXXXXXX/' #Replace with post URL which you want to analyze
shortcode = instaloader.Post.from_shortcode(loader.context, url.split('/')[-2]).shortcode

post = instaloader.Post.from_shortcode(loader.context, shortcode)

comments_list = [{'Username': comment.owner.username, 'Comment': comment.text} for comment in post.get_comments()]

comments_df = pd.DataFrame(comments_list)

def analyze_entity_sentiment(comment):
    doc = spc(comment)
    entities_sentiments = []
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'ORG', 'GPE']:  # Consider only person, organization, and geopolitical entities
            entity_sentiment = TextBlob(ent.text).sentiment.polarity
            sentiment = 'Positive' if entity_sentiment > 0 else 'Negative' if entity_sentiment < 0 else 'Neutral'
            entities_sentiments.append({'Entity': ent.text, 'Sentiment': sentiment})
    return entities_sentiments

comments_df['Entity_Sentiments'] = comments_df['Comment'].apply(analyze_entity_sentiment)

all_comments = ' '.join(comments_df['Comment'])

wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = nltk.corpus.stopwords.words('english'), 
                min_font_size = 10).generate(all_comments)
                        
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
plt.show()

comments_df.to_csv('comments_with_entity_sentiment.csv', index=False)

loader.context.logout()
