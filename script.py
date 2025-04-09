from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit
from h2q import Heatmap
import numpy as np

dim_x = 30
dim_y = 30

prob_heatmap = Heatmap(dim_x=dim_x, dim_y=dim_y)
prob_heatmap.create_gaussian_heatmap()
prob_heatmap.visual()

amps = prob_heatmap.get_amps()
qbits = prob_heatmap.qbits

qc = QuantumCircuit(qbits)
qc.initialize(amps, qc.qubits)
qc.x(range(0, qbits))

state = Statevector.from_instruction(qc)
counts = state.sample_counts(shots=100000)
arr = np.zeros(dim_x * dim_y, dtype=float)
arr_2d = arr.reshape((dim_x, dim_y))

for bs, freq in counts.items():
    index = int(bs, 2)
    try:
        arr[index] = freq
    except:
        pass

new_heatmap = Heatmap()
new_heatmap.use_heatmap(arr_2d)
new_heatmap.visual()