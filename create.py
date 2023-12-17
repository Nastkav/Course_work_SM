import numpy as np

import element as e


class Create(e.Element):
    def __init__(self, name, delay, distribution, delay_dev=None):
        super().__init__(name, delay, distribution, delay_dev)
        self.probability = [1]


    def out_act(self):
        super().out_act()
        self.set_tnext(self.get_tcurr() + self.get_delay())
        selected_element = np.random.choice(a=self.next_element, p=self.probability)
        selected_element.in_act()
        #self.next_element[0].in_act()


