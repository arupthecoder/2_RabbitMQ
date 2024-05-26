import json
import pika

# Define connection parameters
connection_parameters = pika.ConnectionParameters(host='190.2.142.79')

# Connect to RabbitMQ
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

# Define queue names
bbtests_queue_name = 'arindam_BBTestsWorkQueue'
btests_queue_name = 'arindam_BTestsWorkQueue'

# Declare queues (optional)
channel.queue_declare(queue=bbtests_queue_name)
channel.queue_declare(queue=btests_queue_name)

def process_bbtest(message):
  # Decode JSON message
  data = json.loads(message)
  test_name = data["name"]
  tests = data["tests"]
  
  # Push individual tests to BTestsWorkQueue
  for test in tests:
    message = json.dumps({"test": test})
    channel.basic_publish(exchange='', routing_key=btests_queue_name, body=message.encode())
    print(f"[BBManager] Sent test {test} from {test_name} to BTestsWorkQueue")

def on_message_received(ch, method, properties, body):
  process_bbtest(body.decode())
  ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge message

# Consume messages from BBTestsWorkQueue
channel.basic_consume(queue=bbtests_queue_name, on_message_callback=on_message_received)

print("BBManager waiting for messages in BBTestsWorkQueue. Press CTRL+C to exit.")
channel.start_consuming()
