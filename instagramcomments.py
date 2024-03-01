import instaloader
import pandas as pd

user=[]
coment=[]
# Create an Instaloader instance
loader = instaloader.Instaloader()

# Log in to an Instagram account 
loader.context.login('YOUR USERNAME', 'YOUR PASSWORD')

# Target post URL (replace 'post_url' with the URL of the post you want to scrape comments from)
post_url = 'https://www.instagram.com/p/XXXXXXXXXXX/'
shortcode = instaloader.Post.from_shortcode(loader.context, post_url.split('/')[-2]).shortcode

# Get the post by its shortcode
post = instaloader.Post.from_shortcode(loader.context, shortcode)

# Get comments
comments_list = [{'Username': comment.owner.username, 'Comment': comment.text} for comment in post.get_comments()]

# Convert list of comments to DataFrame
comments_df = pd.DataFrame(comments_list)
comments_df.to_csv('comments.csv', index=False)

# Logout
loader.context.close()
