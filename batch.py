import pickle
from pyspark.mllib.recommendation import ALS
from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.mllib.evaluation import RegressionMetrics, RankingMetrics
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType, StringType

spark = SparkSession.builder.appName("Train book recommender 1").getOrCreate()

schema = StructType([StructField("user_id", IntegerType(), True),
                     StructField("book_id", IntegerType(), True),
                     StructField("rating", FloatType(), True)
                    ])
books_df = spark.read.csv('hdfs:///tmp/vycai/ratings.csv', header=True, schema=schema)

id_schema = StructType([StructField("book_id", IntegerType(), True),
                        StructField("goodreads_book_id", IntegerType(), True),
                       ])
id_df = spark.read.csv('hdfs:///tmp/vycai/books.csv', header=True,schema=id_schema).select('book_id', 'goodreads_book_id')

df = books_df.join(id_df, 'book_id')
df = df.select('user_id', 'goodreads_book_id', 'rating')

rank = 100
iterations = 20
l = 0.01
m = ALS.train(df, rank, iterations, l)

pf = m.productFeatures()

pf_vals = pf.sortByKey().values().collect()
pf_keys = pf.sortByKey().keys().collect()

with open(r"pf_vals.pickle", "wb") as output_file:
    pickle.dump(pf_vals, output_file)

with open(r"pf_keys.pickle", "wb") as output_file:
    pickle.dump(pf_keys, output_file)