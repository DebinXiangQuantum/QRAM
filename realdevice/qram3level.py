from qiskit import *
import numpy as np
from qiskit_aer import Aer

AddressBus = QuantumRegister(3,'Ad')
DataBus = QuantumRegister(1,'Data')
classicalData = [0,1,0,1,0,0,0,1]

RouterTwo = QuantumRegister(2,'RT')
RouterDTwo = QuantumRegister(2,'RDT')

RouterThree = QuantumRegister(4,'RTh')
RouterDThree = QuantumRegister(4,'RDTh')

BSM =  ClassicalRegister(2,'BSM')
AddressResult = ClassicalRegister(3,'AR')
DataResult = ClassicalRegister(1,'DR')

CRouterTwo = ClassicalRegister(2,'CRT')
CRouterDTwo = ClassicalRegister(2,'CRDT')
CRouterThree = ClassicalRegister(4,'CRTh')
CRouterDThree = ClassicalRegister(4,'CRDTh')

cir = QuantumCircuit(AddressBus,DataBus,RouterTwo,RouterDTwo,RouterThree,RouterDThree,BSM,AddressResult,DataResult)

#c的状态为|0>
def cswap(a,b,c,mode):
    cir.cswap(a,b,c)
    return None
    if mode==0:
        cir.rx(np.pi,a)
        cir.rz(-1.9344532489776611,b)
        cir.rz(1.214379072189331,c)
        cir.rx(3.124248743057251,b)
        cir.rx(1.5707943439483643,c)
        cir.cz(b,c)
        cir.rz(3.1343448162078857,b)
        cir.rx(0.7853982448577881,b)
        cir.rz(-3.1415913105010986,c)
        cir.rx(1.5881779193878174,c)
        cir.cz(b,c)
        cir.rz(3.1415913105010986,b)
        cir.rx(2.3560431003570557,b)
        cir.cz(a,b)
        cir.rx(np.pi,a)
        cir.rx(2.3560431003570557,b)
        cir.cz(b,c)
        cir.rx(2.3561947345733643,b)
        cir.rx(1.553415060043335,c)
        cir.cz(b,c)
        cir.rx(0.01736760139465332,b)
        cir.rz(1.9268419742584229,b)
        cir.rx(1.5708487033843994,c)
        cir.rz(-1.2143813371658325,c)
    elif mode==1:
        cir.rx(np.pi,a)
        cir.rx(np.pi/2,c)
        cir.cz(a,c)
        cir.rx(np.pi/4,a)
        cir.rx(np.pi/2,c)
        cir.cz(a,b)
        cir.rx(np.pi/4,a)
        cir.rz(-np.pi/2,b)
        cir.rx(np.pi/2,b)
        cir.cz(a,c)
        cir.rz(np.pi/2,a)
        cir.rz(-np.pi/32,c)
        cir.rx(np.pi/2,a)
        cir.rx(np.pi/2,c)
        cir.cz(a,b)
        cir.rz(-3*np.pi/4,a)
        cir.rz(-np.pi/2,b)
        cir.rx(np.pi/2,a)
        cir.rx(np.pi/4,b)
        cir.cz(a,b)
        cir.rx(3.0332618724315243,a)
        cir.rz(-np.pi,b)
        cir.rx(np.pi/2,b)
        cir.cz(a,c)
        cir.rz(-np.pi/2,a)
        cir.rz(np.pi/2,b)
        cir.rx(np.pi/2,c)
        cir.rx(np.pi/2,a)
        cir.cz(a,c)
        cir.rx(np.pi/2,a)
        cir.rx(np.pi/2,c)
        cir.rz(np.pi/32,a)
        cir.rz(8*np.pi/15,c)
   
#a为控制比特，b为左，c为右，d为|0>,mode=0为控制比特处于中心,[[0,1],[0,2],[0,3]]
def cswap_twice(a,b,c,d,mode):
    if mode==0:
        qasm_file_path = 'gates/cswap_control_mid.qasm'
        circuit_from_qasm = QuantumCircuit.from_qasm_file(qasm_file_path)
        cir.compose(circuit_from_qasm, qubits=[a,b,c,d], inplace=True)
    elif mode == 2:
        cir.x(a)
        cir.cswap(a,b,d)
        cir.x(a)
        cir.cswap(a,c,d)


def cx(a,b):
    cir.h(b)
    cir.cz(a,b)
    cir.h(b)

#b的状态为|0>
def swap(a,b):
    cx(a,b)
    cx(b,a)

#mode=0代表左边的子两层QRAM，=1代表右边
def TwoLevelQRAM(RouterQ:list,RDQubit:list,mode):
    root = RouterQ[0]
    leftRouter = RouterQ[1]
    rightRouter = RouterQ[2]
    rootData = RDQubit[0]
    leftData = RDQubit[1]
    rightData = RDQubit[2]
    cswap(root,rootData,rightRouter,mode)
    cir.x(root)
    cswap(root,rootData,leftRouter,mode)
    cir.x(root)
    if mode == 0:
        if classicalData[1]==1:
            cx(leftRouter,leftData)
        if classicalData[3]==1:
            cx(rightRouter,rightData)
        if classicalData[0]==1:
            cir.x(leftRouter)
            cx(leftRouter,leftData)
            cir.x(leftRouter)
        if classicalData[2]==1:
            cir.x(rightRouter)
            cx(rightRouter,rightData)
            cir.x(rightRouter)
    else:
        if classicalData[5]==1:
            cx(leftRouter,leftData)
        if classicalData[7]==1:
            cx(rightRouter,rightData)
        if classicalData[4]==1:
            cir.x(leftRouter)
            cx(leftRouter,leftData)
            cir.x(leftRouter)
        if classicalData[6]==1:
            cir.x(rightRouter)
            cx(rightRouter,rightData)
            cir.x(rightRouter)
    # cswap(root,rightData,rootData,1)
    # cir.x(root)
    # cir.cswap(root,leftData,rootData)
    # cir.x(root)
    cswap_twice(root,leftData,rightData,rootData,mode)

#b,c为Bell态00+11
def teleportation(a,b,c):
    cir.h(b)
    cx(b,c)
    cx(b,a)
    cir.h(b)
    cir.measure(b,BSM[1])
    cir.measure(a,BSM[0])
    cir.x(c).c_if(BSM[0],1)
    cir.z(c).c_if(BSM[1],1)
    cir.reset(a)
    cir.reset(b)

# 制备地址
cir.h(AddressBus[0])
# cir.h(AddressBus[1])
cir.h(AddressBus[2])

cswap(AddressBus[0],AddressBus[1],RouterDTwo[1],1)
cir.x(AddressBus[0])
cswap(AddressBus[0],AddressBus[1],RouterDTwo[0],0)
cir.x(AddressBus[0])
# cir.barrier()
#  ‘；’代表可以并行
swap(RouterDTwo[0],RouterTwo[0]); swap(RouterDTwo[1],RouterTwo[1]); swap(AddressBus[2],AddressBus[1])
# cir.barrier()
cswap(AddressBus[0],AddressBus[1],RouterDTwo[1],1)
cir.x(AddressBus[0])
cswap(AddressBus[0],AddressBus[1],RouterDTwo[0],0)
cir.x(AddressBus[0])
# cir.barrier()

leftTwoQramRouter = [RouterTwo[0],RouterThree[0],RouterThree[1]]
rightTwoQramRouter = [RouterTwo[1],RouterThree[2],RouterThree[3]]
leftTwoQramRouterD = [RouterDTwo[0],RouterDThree[0],RouterDThree[1]]
rightTwoQramRouterD = [RouterDTwo[1],RouterDThree[2],RouterDThree[3]]

# TwoLevelQRAM(leftTwoQramRouter,leftTwoQramRouterD,0); TwoLevelQRAM(rightTwoQramRouter,rightTwoQramRouterD,1)
TwoLevelQRAM(leftTwoQramRouter,leftTwoQramRouterD,2); TwoLevelQRAM(rightTwoQramRouter,rightTwoQramRouterD,2)
# cir.barrier()
cswap(AddressBus[0],RouterDTwo[1],AddressBus[1],1)
cir.x(AddressBus[0])
cswap(AddressBus[0],RouterDTwo[0],AddressBus[1],0)
cir.x(AddressBus[0])
cir.barrier()
# #此处可以使用量子隐形传态
# swap(AddressBus[1],AddressBus[2])
# swap(AddressBus[2],DataBus[0])

teleportation(AddressBus[1],AddressBus[2],DataBus[0])
# cir.swap(AddressBus[1],DataBus[0])

cir.barrier()

cswap(RouterTwo[0],RouterThree[1],RouterDTwo[0],0);cswap(RouterTwo[1],RouterThree[3],RouterDTwo[1],0)
cir.x(RouterTwo[0]);cir.x(RouterTwo[1])
cswap(RouterTwo[0],RouterThree[0],RouterDTwo[0],0);cswap(RouterTwo[1],RouterThree[2],RouterDTwo[1],0)
cir.x(RouterTwo[0]);cir.x(RouterTwo[1])
# cir.barrier()
cswap(AddressBus[0],RouterDTwo[1],AddressBus[1],1)
cir.x(AddressBus[0])
cswap(AddressBus[0],RouterDTwo[0],AddressBus[1],0)
cir.x(AddressBus[0])
swap(AddressBus[1],AddressBus[2])

swap(RouterTwo[0],RouterDTwo[0]); swap(RouterTwo[1],RouterDTwo[1])
cswap(AddressBus[0],RouterDTwo[1],AddressBus[1],1)
cir.x(AddressBus[0])
cswap(AddressBus[0],RouterDTwo[0],AddressBus[1],0)
cir.x(AddressBus[0])

# cir.h(AddressBus[0])
# cir.h(AddressBus[1])
# cir.h(AddressBus[2])
# cswap_twice(AddressBus[0],AddressBus[1],AddressBus[2],DataBus[0],0)
# cswap(AddressBus[0],AddressBus[1],AddressBus[2],0)
# cir.x(AddressBus[0])
# cswap(AddressBus[0],AddressBus[1],AddressBus[2],0)
# cir.x(AddressBus[0])

print(cir.draw())
cir.measure(AddressBus[::-1],AddressResult)
cir.measure(DataBus,DataResult)

exit()
# cir.measure(RouterTwo[::-1],CRouterTwo)
# cir.measure(RouterThree[::-1],CRouterThree)
# cir.measure(RouterDTwo[::-1],CRouterDTwo)
# cir.measure(RouterDThree[::-1],CRouterDThree)
backend=Aer.get_backend('qasm_simulator')
qc_compiled = transpile(cir, backend)
job_sim = backend.run(qc_compiled, shots=10000)
result_sim=job_sim.result()
counts = result_sim.get_counts(qc_compiled)
print(counts)
cz_depth = cir.depth(lambda gate: gate[0].name in ['cz'])
print(cz_depth)
print(cir.count_ops())
print(cir.depth())