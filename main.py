import yaml
from queue import Queue
from queue_network import QueueNetwork

def read_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    config = read_config('config.yml')
    queues = []

    for queue_config in config['queue_configurations']:
        queues.append(
            Queue(
                service_interval_range=queue_config['service_interval_range'],
                servers=queue_config['servers'],
                capacity=queue_config['capacity'],
                id=queue_config['id'],
                arrival_interval_range=queue_config['arrival_interval_range']
            )
        )

    network = QueueNetwork(queues)

    for i in range(len(queues) - 1):
        queues[i].next_queue = queues[i + 1]

    num_events = int(config['events_number'])
    start_time = float(config['start_time'])

    network.simulate(num_events, start_time)

    events_file_path = config['logs_file']
    network.save_events_to_file(events_file_path)
    print(f"\nEventos salvos em: {events_file_path}")

    network.print_statistics()

if __name__ == "__main__":
    main()
