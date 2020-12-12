# MPCS 53014 Final Project
## Available [here!](http://mpcs53014-loadbalancer-217964685.us-east-2.elb.amazonaws.com:3501/)

### Data 
The dataset used in this project is the [goodbooks-10k dataset](https://github.com/zygmuntz/goodbooks-10k), which contains six million Goodreads ratings for the ten thousand most popular books on Goodreads, as of 2017. The total size of the tables used in this project was around 100 MB. 

### Batch Layer
For the batch layer, I used PySpark to train an alternating least squares (ALS) model on the ratings. As it turned out, predicting for new users wasn't a trivial task—the PySpark ALS model doesn't come with built-in functionality for "folding in" users and making predictions for them, so I had to implement this by hand using the product features. The ALS model produces a small set of latent factors that essentially describe products and users, and which can be used to predict products for users, or vice versa. These product features are only 8 MB in size, and can be stored in-memory on our web server. I serialized and saved them in an S3 bucket. 

### Serving Layer
For the serving layer, I used Flask. When a user inputs a Goodreads ID for a user, it retrieves all of that user's ratings using the Goodreads API. It then calculates a best guess latent representation for the new user by multiplying the user's rating vector with the product features, then using that to get predicted ratings for all the items and taking the top `n`. Lastly, it displays the results, fetching the relevant information for each book using the Goodreads API. The steps involving this API are all rather slow, and so results can take several seconds to load. I thought about putting some of the book info (like title, description, and image url, which are shown on the frontend) in Hive, but the description data wasn't available as part of the original dataset I used and Goodreads has measures in place against scraping. 

Homepage:
![](assets/homepage.png)

Sample results:
![](assets/recommendations.png)

### Notes and addenda
The results I got subjectively aren't that good, and there are some quirks. Some books seem to show up far more often than they should, likely because they are overrepresented in the ratings. Some books are just bizarre picks. There may be an issue with my understanding of the ALS model or my linear algebra knowledge, which is extremely shaky at best. I found a comment from a user who questioned whether the ALS model actually produces singular vectors, a critical assumption that I had made, in which case the method I used to find latent representations for new users doesn't actually produce meaningful results. I was searching for explanations in the data, code, and model hyperparameters for the past week, and I only noticed this post at the last minute. If possible, I ask that you take this into consideration when grading. Thank you for reading!
