class FSMController:
def **init**(self, triple, detector\_fn, healer\_fn):
self.triple = triple
self.detect = detector\_fn
self.heal   = healer\_fn
self.state  = "q0"
def step(self):
tags = self.detect(self.triple)
if tags:
for t in tags:
self.triple = self.heal(self.triple, t) if self.triple else None
self.state = "q1" if self.triple else "qX"
else:
self.state = "q2"
return self.state, self.triple
