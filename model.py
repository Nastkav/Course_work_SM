from process import Process
import numpy as np


class Model:
    def __init__(self, elements):
        self.list = elements
        self.t_next = 0.0
        self.event = 0
        self.t_curr = self.t_next
        self.quantity = 0
        self.pause_count = 0

        self.discounts = 0
        self.time_profit = 0
        self.profit = 0
        self.expenses = 0
        self.pause_duration = 0
        self.onetime_expenses = 1000000
        self.money = 0
        self.in_queue = 0

        self.profit_for_one_year = 0
        self.expenses_for_one_year = 0
        self.payback_period = 0

    def simulate(self, time):
        while self.t_curr < time:
            self.t_next = float('inf')

            for e in self.list:
                t_next_val = np.min(e.t_next)
                if t_next_val < self.t_next:
                    self.t_next = t_next_val
                    self.event = e.id

            for e in self.list:
                e.do_statistics(self.t_next - self.t_curr)

            self.t_curr = self.t_next

            for e in self.list:
                e.t_curr = self.t_curr

            if len(self.list) > self.event:
                self.list[self.event].out_act()

            for e in self.list:
                if np.any(self.t_curr == e.t_next):
                    e.out_act()

            self.print_info()

        return self.print_result

    def print_info(self):
        for e in self.list:
            e.print_info()

    @property
    def print_result(self):
        print("\n-------------RESULTS-------------")
        result = list()
        for e in self.list:
            e.print_result()
            result.append(e.get_quantity())
            if isinstance(e, Process):
                p = e
                self.quantity += p.get_quantity()
                self.discounts += p.discount
                self.in_queue += p.count_in_queue
                self.pause_count += p.pause_count
                self.pause_duration = p.pause_duration

                self.profit += p.profit

                print(f"Mean length of queue = {str(p.get_mean_queue() / self.t_curr)}")
                print(f"Failure probability = {str(p.get_failure() / float(p.get_quantity()))}")
                print(f"Remove = {p.remove}")
                print(f"Elements with discount = {p.discount}")
                print(f"Count elements in queue = {p.count_in_queue}")
                print(f"Pause count = {p.pause_count}")
                result.append(
                    [p.get_mean_queue() / self.t_curr, p.get_failure() / float(p.get_quantity()), p.remove, p.discount])
                print()

        print(f"Pause duration = {self.pause_duration}")
        print(f'Discounts = {self.discounts}')
        print(f"One-time expenses = {self.onetime_expenses}")

        self.expenses = self.t_curr - self.time_profit

        self.money = self.profit - self.expenses
        print(self.profit)
        print(self.expenses)
        print(f"Money for day = {self.money}")

        self.expenses_for_one_year = self.expenses * 16 * 365
        self.profit_for_one_year = self.profit * 16 * 365
        self.payback_period = (self.onetime_expenses + self.expenses_for_one_year) / self.profit_for_one_year

        result.append([self.pause_duration, self.money, self.expenses_for_one_year, self.profit_for_one_year,
                       self.payback_period])
        print(f"Payback period (in years) = {self.payback_period}")

        print(result)
        return result
