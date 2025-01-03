from qiskit import *
import math 
from qiskit.quantum_info.operators import Operator
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


ad_bus=QuantumRegister(2,'abus')

data_bus=QuantumRegister(1,'dbus')
ad=QuantumRegister(3,'ad')
data=QuantumRegister(3,'data')
aux=QuantumRegister(3,'aux')
memory=ClassicalRegister(4,'memory')
outcome=ClassicalRegister(3,'outcome')
cir=QuantumCircuit(ad_bus,data_bus,ad,data,aux,memory,outcome)



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
    cir.rx(-math.pi/4,c)
    swap(d,a)
    cir.cz(d,c)
    cir.rx(math.pi/4,c)
    cir.cz(b,c)
    cir.rx(-math.pi/4,c)
    cir.rz(math.pi/4,b)
    cir.h(b)
    cir.cz(d,c)
    swap(a,d)
    cir.cz(a,b)
    cir.rx(math.pi/4,c)
    cir.rz(math.pi/4,a)
    cir.rx(-math.pi/4,b)
    cir.cz(a,b)
    cir.cz(c,b)
    cir.h(b)


arr=[1/2,1/2,1/2,1/2]
cir.initialize(arr,ad_bus[::-1])

swap(data[0],ad_bus[0])
swap(aux[0],data[0])
swap(ad[0],aux[0])

swap(data[0],ad_bus[1])
swap(aux[0],data[0])

cir.x(ad[0])
cswap(ad[0],aux[0],data[1],aux[1])
cir.x(ad[0])

cswap(ad[0],aux[0],data[2],aux[2])

swap(aux[1],data[1])
swap(ad[1],aux[1])

swap(aux[2],data[2])
swap(ad[2],aux[2])

cir.h(data_bus[0])

swap(data[0],data_bus[0])
swap(aux[0],data[0])

cir.x(ad[0])
cswap(ad[0],aux[0],data[1],aux[1])
cir.x(ad[0])

cswap(ad[0],aux[0],data[2],aux[2])

swap(aux[1],ad[1])
swap(aux[2],ad[2])

cir.cz(aux[1],data[1]).c_if(memory[1],1)
cir.x(aux[1])
cir.cz(aux[1],data[1]).c_if(memory[0],1)
cir.x(aux[1])

cir.cz(aux[2],data[2]).c_if(memory[3],1)
cir.x(aux[2])
cir.cz(aux[2],data[2]).c_if(memory[2],1)
cir.x(aux[2])

swap(ad[1],aux[1])
swap(ad[2],aux[2])

cir.x(ad[0])
cswap(ad[0],data[1],aux[0],aux[1])
cir.x(ad[0])

cnot(aux[0],data[2])
cswap(ad[0],data[2],aux[0],aux[2])


swap(data[0],aux[0])
swap(data_bus[0],data[0])
cir.h(data_bus[0])

swap(aux[1],ad[1])
swap(aux[2],ad[2])
swap(data[1],aux[1])
swap(data[2],aux[2])

cir.x(ad[0])
cswap(ad[0],data[1],aux[0],aux[1])
cir.x(ad[0])

cnot(aux[0],data[2])
cswap(ad[0],data[2],aux[0],aux[2])

swap(data[0],aux[0])
swap(ad_bus[1],data[0])

swap(aux[0],ad[0])
swap(data[0],aux[0])
swap(ad_bus[0],data[0])

print(cir.depth())
cir.measure(ad_bus,outcome[2:0:-1])
cir.measure(data_bus,outcome[0])

print(cir)
plt.show()
backend= AerSimulator()
qc_compiled = transpile(cir, backend)
job_sim = backend.run(qc_compiled, shots=1000)
result_sim=job_sim.result()
counts = result_sim.get_counts(qc_compiled)
print(counts)

