from pyspark.sql import SparkSession
from helpers import *

spark = SparkSession.builder \
    .appName("Redpanda Consumer") \
    .config("spark.jars.packages","org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1") \
    .getOrCreate()

def consume(topic):
    # Define your Redpanda servers and topic
    redpanda_brokers = '127.0.0.1:19092'
    print("Starts consuming topic...")

    df = spark \
        .read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", redpanda_brokers) \
        .option("subscribe", topic) \
        .option("startingOffsets", "earliest") \
        .load()
        #
    
    df = df.selectExpr("CAST(value AS STRING)")
    df.show()

    single_row = df.select("value").collect()[-1]
    file_path = single_row.value
    image_path = file_path.split(".")[0] + '.png'
    print(image_path.split('/')[1])
    if not check_file(image_path.split('/')[1]):
        generate_spectrogram(file_path, image_path)

        return image_path