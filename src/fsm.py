class FSMController:
    def __init__(self, triple, detector_fn, healer_fn):
        self.triple = triple
        self.detect = detector_fn
        self.heal   = healer_fn
        self.state  = "q0"
    def step(self):
        tags = self.detect([self.triple])
        if tags:
            for t, rule_tag in tags:
                self.triple = self.heal(self.triple, rule_tag) if self.triple else None
                self.state = "q1" if self.triple else "qX"
        else:
            self.state = "q2"
        return self.state, self.triple
