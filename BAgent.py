import json
import pika

# Define connection parameters
connection_parameters = pika.ConnectionParameters(host='190.2.142.79')

# Connect to RabbitMQ
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

# Define queue name
queue_name = 'arindam_BTestsWorkQueue'

# Declare queue (optional)
channel.queue_declare(queue=queue_name)

# Round robin counter (initialize to 0)
round_robin_counter = 0

def on_message_received(ch, method, properties, body):
  global round_robin_counter
  # Decode JSON message
  data = json.loads(body.decode())
  test = data["test"]
  # Simulate processing based on round robin counter
  print(f"[BAgent {round_robin_counter}] Processing test: {test}")
  # Increment counter for round robin
  round_robin_counter = (round_robin_counter + 1) % num_bagents  # Assuming num_bagents is a global variable set to the number of BAgents

# Consume messages from BTestsWorkQueue
channel.basic_consume(queue=queue_name, on_message_callback=on_message_received)

num_bagents = 2

print("[BAgent] Waiting for tests in queue.")
channel.start_consuming()
