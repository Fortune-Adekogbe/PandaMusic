from kafka import KafkaProducer

def produce(file_path, topic):
    # Create a Producer instance

    print("Creates a Producer instance and send message...", end="")
    producer = KafkaProducer(bootstrap_servers='127.0.0.1:19092', api_version=(2, 0, 2))  # kafka Replace with your Redpanda's address    

    producer.send(topic, value=file_path.encode())

    # Ensure all messages have been sent
    producer.flush()
    print("Done.")