from newspaper import Article
#4b6587f8cd2149e9916c4705ad524c3a
import newspaper

url = "http://www.cnn.com/2017/09/21/politics/kim-jong-un-on-trump-comments/index.html"
article = Article(url)

article.download()

article.parse()

article.publish_date

print(article.title)
