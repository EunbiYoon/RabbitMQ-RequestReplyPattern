import pika
import uuid

def on_reply_message_received(ch, method, properties, body):
    print(f"reply received: {body}")

# open connection
connection_parameters=pika.ConnectionParameters('localhost')
connection=pika.BlockingConnection(connection_parameters)

#create channel
channel=connection.channel()

#declare queue
reply_queue=channel.queue_declare(queue='', exclusive=True)

#consumer queue
channel.basic_consume(queue=reply_queue.method.queue, auto_ack=True,
    on_message_callback=on_reply_message_received)

#send queue
channel.queue_declare(queue='request-queue')

#message
message="Can I request a reply?"
cor_id=str(uuid.uuid4())
print(f"Sending request: {cor_id}")
channel.basic_publish(
    exchange='',
    routing_key='request-queue',
    properties=pika.BasicProperties(
        reply_to=reply_queue.method.queue,
        correlation_id=cor_id),
    body=message)

#check
print(f"Starting Client")

channel.start_consuming()

#close connection
connection.close()