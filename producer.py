import json
import pika


connection_parameters = pika.ConnectionParameters(host='190.2.142.79')

# Connect to RabbitMQ
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

# Define queue name
queue_name = 'arindam_BBTestsWorkQueue'

# Declare queue (optional)
channel.queue_declare(queue=queue_name)

# Define test data (replace with your actual data)
bbtests = {
    "BBTest1": ["T11", "T12", "T13", "T14"],
    "BBTest2": ["T21", "T22", "T23", "T24"],
}

for test_name, test_list in bbtests.items():
  # Convert test data to JSON
  message = json.dumps({"name": test_name, "tests": test_list})
  # Send message to queue
  channel.basic_publish(exchange='', routing_key=queue_name, body=message.encode())
  print(f"[BBApp] Sent message for {test_name} to BBTestsWorkQueue")

connection.close()
