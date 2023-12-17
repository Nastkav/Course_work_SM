import fun_rand as fun


class Element:
    nextId = 0

    def __init__(self, name, delay=None, distribution=None, delay_dev=None):
        self.distribution = distribution
        self.t_next = [0]
        self.t_curr = self.t_next
        self.delay_mean = delay
        self.delay_dev = delay_dev
        self.quantity = 0
        self.state = [0]
        self.next_element = None
        self.id = Element.nextId
        Element.nextId += 1
        self.name = name

    def get_delay(self):
        if 'exp' == self.distribution:
            return fun.exp(self.delay_mean)
        elif 'norm' == self.distribution:
            return fun.norm(self.delay_mean, self.delay_dev)
        elif 'uniform' == self.distribution:
            return fun.uniform(self.delay_mean, self.delay_dev)
        elif 'erlang' == self.distribution:
            return fun.erlang(self.delay_mean, self.delay_dev)
        else:
            return self.delay_mean

    def get_delay_dev(self):
        return self.delay_dev

    def set_delay_dev(self, delay_dev):
        self.delay_dev = delay_dev

    def get_distribution(self):
        return self.distribution

    def set_distribution(self, distribution):
        self.distribution = distribution

    def get_quantity(self):
        return self.quantity

    def get_tcurr(self):
        return self.t_curr

    def set_tcurr(self, t_curr):
        self.t_curr = t_curr

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def in_act(self):
        pass

    def out_act(self):
        self.quantity += 1

    def get_tnext(self):
        return self.t_next

    def set_tnext(self, t_next):
        self.t_next = t_next

    def get_delay_mean(self):
        return self.delay_mean

    def set_delay_mean(self, delay_mean):
        self.delay_mean = delay_mean

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def print_result(self):
        print(self.name + " quantity = " + str(self.quantity))

    def print_info(self):
        print(self.name + " state= " + str(self.state) + " quantity = " + str(self.quantity) + " tnext= " + str(
            self.t_next))

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def do_statistics(self, delta):
        pass
