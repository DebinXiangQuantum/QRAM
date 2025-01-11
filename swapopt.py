from qiskit import QuantumCircuit,transpile
from numpy import pi
from qiskit_aer import Aer
cir = QuantumCircuit(3)
# cir.x(0)
# cir.h(1)
# cir.h(2)
cir.cswap(0,1,2)
print(cir)
opt_circ = transpile(cir, basis_gates=['rz','cz','h'], coupling_map=[[0,1],[1,2]], optimization_level=1)
# opt_circ = transpile(cir, basis_gates=['rz','cz','h'],  optimization_level=1)
print(opt_circ)
print(opt_circ.count_ops())
print(opt_circ.depth())
opt_circ.measure_all()
simulator = Aer.get_backend('qasm_simulator')
result = simulator.run(transpile(opt_circ, simulator)).result()
counts = result.get_counts(opt_circ)

## cpflow opt
import numpy as np
from cpflow import *

u_target = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                     [0, 1, 0, 0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 1, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 1, 0],
                     [0, 0, 0, 0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 1]])
layer = [[0, 1], [0, 2]]  # Linear connectivity
decomposer = Synthesize(layer, target_unitary=u_target, label='cswap')
options = StaticOptions(num_cp_gates=18, accepted_num_cz_gates=12, num_samples=20)
results = decomposer.static(options) # Should take from one to five minutes.

d = results.decompositions[0]  # This turned out to be the best decomposition for refinement.
d.refine()
print(d)
print(d.circuit.draw())
circuit : QuantumCircuit = d.circuit
circuit.qasm(formatted=True,filename='cswap.qasm')
print(counts)
def cnot(a,b):
    cir.h(b)
    cir.cz(a,b)
    cir.h(b)
    
def swap(a,b):
    cir.iswap(a,b)
    cir.s(a).inverse()
    cir.s(b).inverse()

def cswap(a,b,c,d): #第三位为|0>
    cir.cz(b,c)
    cir.rx(-pi/4,c)
    swap(d,a)
    cir.cz(d,c)
    cir.rx(pi/4,c)
    cir.cz(b,c)
    cir.rx(-pi/4,c)
    cir.rz(pi/4,b)
    cir.h(b)
    cir.cz(d,c)
    swap(a,d)
    cir.cz(a,b)
    cir.rx(pi/4,c)
    cir.rz(pi/4,a)
    cir.rx(-pi/4,b)
    cir.cz(a,b)
    cir.cz(c,b)
    cir.h(b)

# cswap(0,1,2,3)
# circ_opt, results = qmap.optimize_clifford(cir)
# print(circ_opt)
# print(results)