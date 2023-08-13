from consumer import spark, consume, upload_and_produce

spark.sparkContext.setLogLevel("ERROR")


print("Start streaming.")

while True:
    bucket = "panda-spectrogram"
    topic = "music_ingested"
    image_path = consume(topic=topic)
    if image_path is not None:
        topic = "music_processed"
        
        upload_and_produce(
            image_path=image_path, topic=topic, bucket=bucket
        )
    else:
        print("File already exists.")
        break
print("End streaming.")