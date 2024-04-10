import numpy as np

class Queue:
    def __init__(
        self,
        service_interval_range,
        servers,
        capacity,
        id,
        arrival_interval_range=(1, 4),
        next_queue=None,
    ):
        self.service_interval_range = service_interval_range
        self.arrival_interval_range = arrival_interval_range
        self.servers = servers
        self.capacity = capacity
        self.id = id
        self.next_queue = next_queue
        self.queue = []
        self.in_service = []
        self.completed = 0
        self.lost = 0
        self.total_service_time = 0
        self.total_customers_arrived = 0
        self.customer_id = 0
        self.events = []

    def generate_service_time(self):
        return np.random.uniform(*self.service_interval_range)

    def process_arrival(self, time):
        self.customer_id += 1
        if len(self.queue) + len(self.in_service) < self.capacity:
            self.queue.append((self.customer_id, time))
            self.events.append(
                f"[Tempo {time:.2f}]: Cliente {self.customer_id} chegou à Fila {self.id}"
            )
        else:
            self.lost += 1
            self.events.append(
                f"[Tempo {time:.2f}]: Cliente {self.customer_id} perdido na Fila {self.id}"
            )

    def start_service(self, current_time):
        while len(self.in_service) < self.servers and self.queue:
            customer_id, arrival_time = self.queue.pop(0)
            service_time = self.generate_service_time()
            self.total_service_time += service_time
            departure_time = current_time + service_time
            self.in_service.append((customer_id, departure_time))
            self.events.append(
                f"[Tempo {current_time:.2f}]: Cliente {customer_id} iniciou o serviço na Fila {self.id}"
            )

    def process_departures(self, current_time):
        for customer in list(self.in_service):
            if customer[1] <= current_time:
                self.in_service.remove(customer)
                self.completed += 1
                self.events.append(
                    f"[Tempo {current_time:.2f}]: Cliente {customer[0]} completou o serviço na Fila {self.id}"
                )
                if self.next_queue is not None:
                    self.next_queue.process_arrival(customer[1])

    def statistics(self, total_time):
        total_customers = self.completed + self.lost
        percent_lost = (self.lost / total_customers * 100) if total_customers else 0
        percent_completed = (
            (self.completed / total_customers * 100) if total_customers else 0
        )
        average_service_time = (
            (self.total_service_time / self.completed) if self.completed else 0
        )
        return (
            percent_lost,
            percent_completed,
            total_customers,
            total_time,
            average_service_time,
        )
