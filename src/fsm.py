class FSMController:
    """Finite-state wrapper for a single triple."""
    def __init__(self, triple, detector_fn, healer_fn):
        self.triple = triple
        self.detect = detector_fn
        self.heal   = healer_fn
        self.state  = "q0"  # assume infected until checked

    def step(self):
        tags = self.detect(self.triple)
        if tags:                       # infection(s) present
            for t in tags:
                self.triple = self.heal(self.triple, t) if self.triple else None
            self.state = "q1" if self.triple else "qX"
        else:
            self.state = "q2"
        return self.state, self.triple
