from copy import deepcopy
from datetime import datetime

import numpy as np
import element as e


class Process(e.Element):
    def __init__(self, name, delay=None, distribution=None, delay_dev=None, max_pause_count=100000, maxi_queue=100000):
        super().__init__(name, delay, distribution, delay_dev)
        self.queue = 0
        self.max_queue = maxi_queue
        self.mean_queue = 0.0
        self.failure = 0
        self.state = 0
        self.t_next = np.inf
        self.probability = [1]
        self.priority = [1]

        self.pause_interval_start = 15
        self.change_pause_interval_start = self.pause_interval_start
        self.is_pause = False  # 1-pause, 0-radio

        self.curr_pause_duration = 0
        self.max_pause_duration = 0.1 * 16 * 60

        self.max_pause_count = max_pause_count  # self.max_pause_duration / self.pause_duration
        self.pause_duration = 0#self.max_pause_duration / self.max_pause_count  # 3 # тривалість пауз однакова, к-сть пауз задати самостійно
        self.pause_count = 0

        self.max_queue_time = 4 * 60
        self.time_el_in_queue = [None] * self.max_queue
        self.remove = 0

        self.discount = 0
        self.delay = 0
        self.time_profit = 0

        self.count_in_queue = 0

        self.profit = 0

    def update_speaker(self):
        if self.t_curr >= self.change_pause_interval_start and self.curr_pause_duration < self.max_pause_duration \
                and self.pause_count < self.max_pause_count:
            self.change_pause_interval_start += self.pause_interval_start
            print(f'CHECK PAUSE {self.is_pause}')
            self.is_pause = True
            self.pause_count += 1
            self.curr_pause_duration += self.pause_duration

    def choose_by_priority(self):
        priorities = deepcopy(self.priority)
        min_queue = float('inf')
        with_min_q_index = 0
        for p in range(len(priorities)):
            if min(priorities) == float('inf'):
                break
            pr_index = priorities.index(min(priorities))
            if 0 in self.next_element[pr_index].state:
                return self.next_element[pr_index]
            else:
                if min_queue > self.next_element[pr_index].queue:
                    min_queue = self.next_element[pr_index].queue
                    with_min_q_index = self.next_element.index(self.next_element[pr_index])

            priorities[pr_index] = 10000000
        return self.next_element[with_min_q_index]

    def choose_next_el(self):
        if self.probability == [1] and self.priority == [1]:
            return self.next_element[0]
        elif self.probability != [1] and self.priority != [1]:
            raise Exception('Error: Probability and priority are both defined.')
        elif self.probability != [1]:
            next_element = np.random.choice(a=self.next_element, p=self.probability)
            return next_element
        elif self.priority != [1]:
            next_element = self.choose_by_priority()
            return next_element

    def in_act(self):
        self.update_speaker()
        if self.state == 0 and self.is_pause:
            self.state = 1
            self.delay = self.get_delay()
            self.time_profit += self.delay
            if self.delay > self.pause_duration:
                self.discount += 1
                self.profit += 0.9 * self.delay * 300
                self.t_next = self.t_curr + self.delay
                self.is_pause = False
            else:
                self.delay = self.get_delay()
                self.profit += self.delay * 300
                self.t_next = self.t_curr + self.delay
                self.is_pause = False
        else:
            if self.queue < self.max_queue:
                self.queue += 1
                self.count_in_queue += 1
                self.time_el_in_queue[self.queue - 1] = self.t_curr
            else:
                self.failure += 1

    def out_act(self):
        super().out_act()
        self.t_next = np.inf
        self.state = 0
        for i, time_in_queue in enumerate(self.time_el_in_queue):
            if time_in_queue is not None and self.t_curr - time_in_queue >= self.max_queue_time:
                print('!!!=========================!!!')
                print(f'Element removed from the queue: {self.name}')
                time_spent_in_queue = self.t_curr - time_in_queue
                print(f'Time spent in queue: {time_spent_in_queue}')
                self.queue -= 1
                self.remove += 1
                self.time_el_in_queue[i] = None
                self.failure += 1
        if self.queue > 0 and self.is_pause:
            self.profit += 0.7 * self.delay * 300
            self.queue -= 1
            self.state = 1
            self.delay = self.get_delay()
            self.t_next = self.t_curr + self.delay
            self.time_profit += self.delay
        if self.next_element is not None:
            next_el = self.choose_next_el()
            next_el.in_act()

    def get_failure(self):
        return self.failure

    def get_queue(self):
        return self.queue

    def set_queue(self, queue):
        self.queue = queue

    def get_max_queue(self):
        return self.max_queue

    def set_max_queue(self, max_queue):
        self.max_queue = max_queue

    def print_info(self):
        super().print_info()
        print(f'failure= {str(self.failure)}, queue= {str(self.queue)}')

    def get_mean_queue(self):
        return self.mean_queue

    # zmin. pid task 2
    def do_statistics(self, delta):

        self.mean_queue = self.get_mean_queue() + self.queue * delta

        # for i in range(self.channel):
        #     self.mean_load += self.state[i] * delta
        #
        # self.mean_load = self.mean_load / self.channel
