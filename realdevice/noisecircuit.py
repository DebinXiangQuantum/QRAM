import numpy as np
import pickle   
from qiskit import QuantumCircuit,ClassicalRegister,QuantumRegister, transpile
from qiskit_aer import AerSimulator

# Import from Qiskit Aer noise module
from qiskit_aer.noise import NoiseModel
from qiskit_aer.noise import ReadoutError
from qiskit_aer.noise import pauli_error
from qiskit_aer.noise import depolarizing_error

def fidelity2lambda_depolar(fidelity,num_qubits=1):
    N = 2**num_qubits
    param = (fidelity*N-1)/(N-1)
    print(1-param)
    return 1-param

p_reset = 0.03
p_meas = 0.0085
p_gate_cz = 0.0054
p_gate_single = 0.0008
a=np.sqrt(1-p_gate_cz)
# 量子错误对象
error_reset = pauli_error([('X', p_reset), ('I', 1 - p_reset)])
error_meas = ReadoutError([[0.9915,0.0085],[0.0085,0.9915]])


error_gate1 =  depolarizing_error(fidelity2lambda_depolar(1-p_gate_single), 1)
error_gate_cz = depolarizing_error(fidelity2lambda_depolar(1-p_gate_single,num_qubits=2), 2)

# 添加错误到噪声模型
noise_bit_flip = NoiseModel(basis_gates=['cz', 'id', 'rx','h','ry','u3','initialize','reset'])
noise_bit_flip.add_all_qubit_quantum_error(error_gate1, ['id', 'rx','h','ry','u3'])
noise_bit_flip.add_all_qubit_quantum_error(error_reset, "reset")
noise_bit_flip.add_all_qubit_readout_error(error_meas)
noise_bit_flip.add_all_qubit_quantum_error(error_gate_cz, ["cz"])

with open('./couple_cz.pkl','rb') as f:
    couple_cz=pickle.load(f)

def Qram(address,classicalData,mea_num,mea_basis=80,noise=True):
    AddressBus = QuantumRegister(3,'Ad')
    DataBus = QuantumRegister(1,'Data')
    RouterTwo = QuantumRegister(2,'RT')
    RouterDTwo = QuantumRegister(2,'RDT')

    RouterThree = QuantumRegister(4,'RTh')
    RouterDThree = QuantumRegister(4,'RDTh')

    # BSM =  ClassicalRegister(2,'BSM')
    AddressResult = ClassicalRegister(3,'AR')
    DataResult = ClassicalRegister(1,'DR')

    cir = QuantumCircuit(AddressBus,DataBus,RouterTwo,RouterDTwo,RouterThree,RouterDThree,
                        #  BSM,
                         AddressResult,DataResult)

    def check_connect(couple_cz):
        t=True
        for gate in cir.data:
            if gate[0].name == 'cz':
                if gate[1] not in couple_cz:
                    t=False
                    break
        return t

    #c的状态为|0>
    def cswap(a,b,c,mode):
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
        elif mode == 2:
            qasm_file_path = './cswap_102.qasm'
            circuit_from_qasm = QuantumCircuit.from_qasm_file(qasm_file_path)
            cir.compose(circuit_from_qasm, qubits=[a,b,c], inplace=True)
        elif mode == 3:
            qasm_file_path = './cswap_201.qasm'
            circuit_from_qasm = QuantumCircuit.from_qasm_file(qasm_file_path)
            cir.compose(circuit_from_qasm, qubits=[a,b,c], inplace=True)
    #a为控制比特，b为左，c为右，d为|0>,mode=0为控制比特处于中心,[[0,1],[0,2],[0,3]]
    def cswap_twice(a,b,c,d,mode):
        if mode==0:
            qasm_file_path = './cswap_control_mid.qasm'
            circuit_from_qasm = QuantumCircuit.from_qasm_file(qasm_file_path)
            cir.compose(circuit_from_qasm, qubits=[a,b,c,d], inplace=True)

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
        cswap(root,rootData,rightRouter,0)
        cir.x(root)
        cswap(root,rootData,leftRouter,0)
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
        # cswap(root,leftData,rootData,0)
        # cir.x(root)
        cswap_twice(root,leftData,rightData,rootData,0)

    #b,c为Bell态00+11
    def teleportation(a,b,c, BSM):
        cir.h(b)
        cx(b,c)
        cx(b,a)
        cir.h(b)
        cir.measure(b,BSM[1])
        cir.measure(a,BSM[0])
        # cir.x(c).c_if(BSM[0],1)   
        # cir.z(c).c_if(BSM[1],1)
        cir.reset(a)
        cir.reset(b)

    def rotate(q,single_mea_basis):
        if single_mea_basis == '0':
            cir.ry(-np.pi/2,q)
        elif single_mea_basis == '1':
            cir.rx(np.pi/2,q)
    
    def TenToThree(num,width):
        string = ''
        t=0
        while num != 0 or t<width:
            num,s = divmod(num,3)
            string = str(s) + string
            t=t+1
        return string

    def rotate_all(mea_basis):
        a = TenToThree(mea_basis,4)
        for i in range(4):
            single_mea_basis = a[i]
            if i != 3:
                rotate(AddressBus[i],single_mea_basis)
            else:
                rotate(DataBus[0],single_mea_basis)


    #制备地址
    cir.initialize(address,AddressBus[::-1])
    # cir.x(AddressBus[0])
    # cir.x(AddressBus[2])
    # cir.x(AddressBus[1])

    cswap(AddressBus[0],AddressBus[1],RouterDTwo[1],1)
    cir.x(AddressBus[0])
    cswap(AddressBus[0],AddressBus[1],RouterDTwo[0],0)
    cir.x(AddressBus[0])
    # cswap(AddressBus[0],AddressBus[1],RouterDTwo[1],3)
    # cir.barrier()
    #  ‘；’代表可以并行
    swap(RouterDTwo[0],RouterTwo[0]); swap(RouterDTwo[1],RouterTwo[1]); swap(AddressBus[2],AddressBus[1])
    # cir.barrier()
    cswap(AddressBus[0],AddressBus[1],RouterDTwo[1],1)
    cir.x(AddressBus[0])
    cswap(AddressBus[0],AddressBus[1],RouterDTwo[0],0)
    cir.x(AddressBus[0])
    # cswap(AddressBus[0],AddressBus[1],RouterDTwo[1],3)
    # cir.barrier()

    leftTwoQramRouter = [RouterTwo[0],RouterThree[0],RouterThree[1]]
    rightTwoQramRouter = [RouterTwo[1],RouterThree[2],RouterThree[3]]
    leftTwoQramRouterD = [RouterDTwo[0],RouterDThree[0],RouterDThree[1]]
    rightTwoQramRouterD = [RouterDTwo[1],RouterDThree[2],RouterDThree[3]]

    TwoLevelQRAM(leftTwoQramRouter,leftTwoQramRouterD,0); TwoLevelQRAM(rightTwoQramRouter,rightTwoQramRouterD,1)
    # cir.barrier()
    # cswap(AddressBus[0],RouterDTwo[1],AddressBus[1],3)
    cswap(AddressBus[0],RouterDTwo[1],AddressBus[1],1)
    cir.x(AddressBus[0])
    cswap(AddressBus[0],AddressBus[1],RouterDTwo[0],0)
    cir.x(AddressBus[0])
    # cir.barrier()
    # #此处可以使用量子隐形传态
    swap(AddressBus[1],AddressBus[2])
    swap(AddressBus[2],DataBus[0])

    # teleportation(AddressBus[1],AddressBus[2],DataBus[0])
    # cir.barrier()

    cswap(RouterTwo[0],RouterDTwo[0],RouterThree[1],0);cswap(RouterTwo[1],RouterDTwo[1],RouterThree[3],0)
    cir.x(RouterTwo[0]);cir.x(RouterTwo[1])
    cswap(RouterTwo[0],RouterDTwo[0],RouterThree[0],0);cswap(RouterTwo[1],RouterDTwo[1],RouterThree[2],0)
    cir.x(RouterTwo[0]);cir.x(RouterTwo[1])
    # cir.barrier()
    cswap(AddressBus[0],RouterDTwo[1],AddressBus[1],1)
    cir.x(AddressBus[0])
    cswap(AddressBus[0],AddressBus[1],RouterDTwo[0],0)
    cir.x(AddressBus[0])
    swap(AddressBus[1],AddressBus[2])

    swap(RouterTwo[0],RouterDTwo[0]); swap(RouterTwo[1],RouterDTwo[1])
    cswap(AddressBus[0],RouterDTwo[1],AddressBus[1],1)
    cir.x(AddressBus[0])
    cswap(AddressBus[0],AddressBus[1],RouterDTwo[0],0)
    cir.x(AddressBus[0])

    rotate_all(mea_basis)

    cir.measure(AddressBus[::-1],AddressResult)
    cir.measure(DataBus,DataResult)
    if noise:
        noise_model = AerSimulator(noise_model=noise_bit_flip)
        qc_compiled = transpile(cir, noise_model)
        print(qc_compiled.depth())
        print(qc_compiled.count_ops())
        # print(qc_compiled)
        job_sim = noise_model.run(qc_compiled,shots=mea_num).result()
        counts_noise = job_sim.get_counts(0)
        if check_connect(couple_cz):
            return counts_noise
        else:
            return False
    else:
        noise_model = AerSimulator()
        qc_compiled = transpile(cir)
        print(qc_compiled.depth())
        print(qc_compiled.count_ops())
        job_sim = noise_model.run(qc_compiled,shots=mea_num).result()
        counts = job_sim.get_counts(0)
        if check_connect(couple_cz):
            return counts
        else:
            return False

def generate_random_address(num_qubits):
    random_choice = np.random.choice(2**num_qubits)
def generate_random_data(data):
    pass

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description='QRAM in noise model')
    parser.add_argument(
        '--noise', type=bool, default=False,
        help='Use noise model or not')
    args = parser.parse_args()
    address = [0,0,0,0,0,0,1,1]/np.sqrt(2)
    data = [1,0,1,0,1,0,1,0]
    counts = Qram(address,data,100000,noise=args.noise)
    print(counts)