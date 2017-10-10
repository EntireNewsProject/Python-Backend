from newspaper import Article
#4b6587f8cd2149e9916c4705ad524c3a
import requests
import newspaper

url = "https://newsapi.org/v1/articles?source=techcrunch&apiKey=4b6587f8cd2149e9916c4705ad524c3a"

article = Article(url)

article.download()

article.parse()




print (url)

article.publish_date

print(article.title)
