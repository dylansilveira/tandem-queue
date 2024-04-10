import numpy as np

class QueueNetwork:
    def __init__(self, queues):
        self.queues = queues

    def simulate(self, num_events, start_time):
        time = start_time
        self.queues[0].process_arrival(time)
        for _ in range(num_events - 1):
            time += np.random.exponential(1)
            self.queues[0].process_arrival(time)
            for queue in self.queues:
                queue.start_service(time)
                queue.process_departures(time)
        self.total_time = time

    def save_events_to_file(self, filename):
        with open(filename, "w") as file:
            for queue in self.queues:
                for event in queue.events:
                    file.write(event + "\n")

    def print_statistics(self):
        for queue in self.queues:
            stats = queue.statistics(self.total_time)
            print(f"\nEstatísticas da Fila {queue.id}:")
            print(f"Percentual de Perda: {stats[0]:.2f}%")
            print(f"Percentual de Completude: {stats[1]:.2f}%")
            print(f"Total de Clientes: {stats[2]}")
            print(f"Tempo Total: {stats[3]:.2f}")
            print(f"Tempo Médio de Serviço: {stats[4]:.2f}")
