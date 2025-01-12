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

memory=ClassicalRegister(4,'memory')
outcome=ClassicalRegister(3,'outcome')
cir=QuantumCircuit(ad_bus,data_bus,ad,data,aux,memory,outcome)

from numpy import pi

def double_teleportation(q):
    """
    a,b,c,d are the quantum registers for the input and output
    q[0]: input qubit 
    q[1]: control qubit
    q[2]: target qubit 1
    q[3]: target qubit 2
    """
    cir.rz(pi/2, q[0])
    cir.rx(pi/2, q[0])
    cir.rz(2.178722620010376, q[1])
    cir.rx(2.1034767627716064, q[1])
    cir.cz( q[0],q[1])
    cir.x(q[0])
    cir.rz(-2.2012643814086914, q[1])
    cir.rx(0.7853977680206299, q[1])
    cir.cz( q[1],q[3])
    cir.rz(0.046204566955566406, q[1])
    cir.rx(2.838059663772583, q[1])
    cir.cz( q[0],q[1])
    cir.rz(0.03687000274658203, q[1])
    cir.rx(2.3561336994171143, q[1])
    cir.cz( q[0],q[1])
    cir.rz(-0.02375936508178711, q[1])
    cir.rx(2.6593563556671143, q[1])
    cir.cz( q[1],q[2])
    cir.rz(3.1095221042633057, q[1])
    cir.rx(2.3561952114105225, q[1])
    cir.cz( q[1],q[3])
    cir.rx(0.7853982448577881, q[1])
    cir.cz( q[0],q[1])
    cir.rx(pi/2, q[0])
    cir.rx(0.7853972911834717, q[1])
    cir.cz( q[1],q[3])
    cir.rx(2.3561947345733643, q[1])
    cir.cz( q[0],q[1])
    cir.rz(pi/2, q[0])
    cir.rx(3.1305735111236572, q[0])
    cir.x(q[1])
    cir.cz( q[1],q[2])
    cir.rz(2.3609917163848877, q[1])
    cir.rx(pi/2, q[1])
    cir.rz(pi/2, q[1])
    cir.z(q[2])
    cir.h(q[0])
    cir.measure(q[0],0)
    cir.z(q[2]).c_if(0,1)
    cir.z(q[3]).c_if(0,1)

def reverse_double_teleportation(q):
    """
    q[0]: input qubit 
    q[1]: control qubit
    q[2]: target qubit 1
    q[3]: target qubit 2
    """
    pass
    


def cnot(a,b):
    cir.h(b)
    cir.cz(a,b)
    cir.h(b)
    
def cswap(q):
    cir.rz(1.9986164569854736,q[1])
    cir.rx(0.1859593391418457,q[1])
    cir.cz( q[0],q[1])
    cir.rx(3.1414453983306885,q[0])
    cir.rz(0.39461636543273926,q[1])
    cir.rx(1.570793867111206,q[1])
    cir.rz(-2.325270414352417,q[2])
    cir.rx(1.4996445178985596,q[2])
    cir.cz( q[1],q[2])
    cir.rz(-3.141577959060669,q[1])
    cir.rx(2.356193780899048,q[1])
    cir.cz( q[0],q[1])
    cir.rx(3.141592264175415,q[0])
    cir.rz(-3.1415770053863525,q[1])
    cir.rx(0.8390493392944336,q[1])
    cir.rz(1.6863858699798584,q[2])
    cir.rx(1.6270678043365479,q[2])
    cir.cz( q[1],q[2])
    cir.rz(-1.5705323219299316,q[1])
    cir.rx(1.5710699558258057,q[1])
    cir.rz(-2.3577821254730225,q[2])
    cir.rx(1.5707881450653076,q[2])
    cir.cz( q[1],q[2])
    cir.rz(2.3577845096588135,q[1])
    cir.rx(1.6270687580108643,q[1])
    cir.cz( q[0],q[1])
    cir.rz(0.785407304763794,q[0])
    cir.rz(-1.5144445896148682,q[1])
    cir.rx(0.7853965759277344,q[1])
    cir.rx(1.5707967281341553,q[2])
    cir.cz( q[1],q[2])
    cir.rx(0.7854020595550537,q[1])
    cir.rz(-1.6244618892669678,q[2])
    cir.rx(1.5710680484771729,q[2])
    cir.cz( q[1],q[2])
    cir.rz(-0.1719667911529541,q[1])
    cir.rx(1.4999163150787354,q[1])
    cir.rz(-0.8163588047027588,q[1])
    cir.rz(-1.4985880851745605,q[2])
    cir.rx(1.399273157119751,q[2])
    cir.rz(-2.39945387840271,q[2])


arr=[1/2,1/2,1/2,1/2]
cir.initialize(arr,ad_bus[::-1])

swap(data[0],ad_bus[0])

double_teleportation(ad_bus[1],data[0],data[1],data[2])

swap(data_bus[0],ad[0])

double_teleportation(ad[0],data[0],ad[1],ad[2])



cir.cz(data[1],ad[1]).c_if(memory[1],1)
cir.x(data[1])
cir.cz(data[1],ad[1]).c_if(memory[0],1)
cir.x(data[1])

cir.cz(data[2],ad[2]).c_if(memory[3],1)
cir.x(data[2])
cir.cz(data[2],ad[2]).c_if(memory[2],1)
cir.x(data[2])




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

