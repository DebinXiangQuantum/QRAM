from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np


class RouterQubit:
    def __init__(self, x, y, level, direction):
        self.x = x
        self.y = y
        self.level = level
        self.left_router = None
        self.right_router = None
        self.left = None
        self.right = None
        self.root = None
        self.direction = direction
        self.qreg = QuantumRegister(1,self.reg_name)

    def add_left(self,pos_x, pos_y):
        self.left = RouterQubit(pos_x, pos_y,self.level+1, self.direction + '0')
        self.left.parent = self.left_router
        self.left_router.next = self.left
    
    def add_right(self,pos_x, pos_y):
        self.right = RouterQubit(pos_x, pos_y, self.level+1, self.direction + '1')
        self.right.parent = self.right_router
        self.right_router.next = self.right
    
    def add_left_router(self, pos_x, pos_y):
        self.left_router = RouterQubit(pos_x, pos_y,  self.level+1, self.direction + 'l')
        self.left_router.parent = self
    
    def add_right_router(self, pos_x, pos_y):
        self.right_router = RouterQubit(pos_x, pos_y,  self.level+1, self.direction + 'r')
        self.right_router.parent = self
        
        
        

    @property
    def address(self):
        if self.root is None:
            return self.direction
        else:
            return self.root.address + self.direction

    @property
    def reg_name(self):
        if self.address:
            return f"router_{self.level}_{self.address}"
        else:
            return f"router_{self.level}"

    def add_leaf_qubits(self, circuit):
        self.left =  QuantumRegister(1,self.reg_name + '_l')
        self.right =  QuantumRegister(1,self.reg_name + '_r')
        circuit.add_register(self.left)
        circuit.add_register(self.right)
    
    def add_data_qubits(self, circuit):
        self.data =  QuantumRegister(1,self.reg_name + '_data')
        circuit.add_register(self.data)


def map_h_tree_to_grid(node: RouterQubit, x, y, length, depth):
    """
    递归地将 H 树映射到网格。

    :param x: 当前 H 树的中心 x 坐标
    :param y: 当前 H 树的中心 y 坐标
    :param length: 当前 H 树的水平线段长度
    :param depth: 剩余的递归深度（可以是半整数）
    :param result: 存储线段起点和终点的列表
    :param grid_mapping: 存储 H 树顶点与网格格点映射关系的字典
    :return: 返回当前节点
    """
    if depth <= 0:
        print('min length:', length/2)
        return None

    half_length = length / 2

    # 当前 H 的线段坐标
    left_x = x - half_length
    half_left_x = x - half_length/2
    right_x = x + half_length
    half_right_x = x + half_length/2
    
    top_y = y + half_length
    half_top_y = y + half_length/2
    bottom_y = y - half_length
    half_bottom_y = y - half_length/2
    
    if depth*2 % 2 == 0 and depth > 1:
        left_x = left_x + half_length/4
        # half_left_x = half_left_x + half_length/4
        right_x = right_x - half_length/4
        # half_right_x = half_right_x - half_length/4
    elif depth*2 % 2 == 1 and depth > 1:
        top_y = top_y - half_length/4
        # half_top_y = half_top_y - half_length/4
        bottom_y = bottom_y + half_length/4
        # half_bottom_y = half_bottom_y + half_length/4
        

    # 水平线段
    if depth == 0.5:
        print('min length:', length/2)
        node.add_left_router(left_x, y)
        node.add_left(left_x,node.parent.y)
        # 右垂直线段
        node.add_right_router(right_x, y)
        node.add_right(right_x,node.parent.y)
        node.min_length = length/2
        return node
    # 左垂直线段
    node.add_left_router(half_left_x, y)
    node.add_left(left_x,y)
    # 右垂直线段
    node.add_right_router(half_right_x, y)
    node.add_right(right_x,y)
    if depth > 1:
        node.left.add_left_router(left_x, half_bottom_y)
        node.left.add_left(left_x, bottom_y)
        map_h_tree_to_grid(node.left.left,left_x, bottom_y, length / 2, depth - 1)  # 左下
        
        node.left.add_right_router(left_x, half_top_y)
        node.left.add_right(left_x, top_y)
        map_h_tree_to_grid(node.left.right,left_x, top_y, length / 2, depth - 1)
        
        node.right.add_left_router(right_x, half_bottom_y)
        node.right.add_left(right_x, bottom_y)
        map_h_tree_to_grid(node.right.left,right_x, bottom_y, length / 2, depth - 1) # 右下
        
        node.right.add_right_router(right_x, half_top_y)
        node.right.add_right(right_x, top_y)
        map_h_tree_to_grid(node.right.right,right_x, top_y, length / 2, depth - 1) # 右上
    if depth == 1:
        node.left.add_left_router(left_x, bottom_y)
        node.left.add_left(node.left.parent.x, bottom_y)
        map_h_tree_to_grid(node.left.left,left_x, bottom_y, length / 2, depth - 1)  # 左下
        
        node.left.add_right_router(left_x, top_y)
        node.left.add_right(node.left.parent.x, top_y)
        map_h_tree_to_grid(node.left.right,left_x, top_y, length / 2, depth - 1)
        
        node.right.add_left_router(right_x, bottom_y)
        node.right.add_left(node.right.parent.x, bottom_y)
        map_h_tree_to_grid(node.right.left,right_x, bottom_y, length / 2, depth - 1) # 右下
        
        node.right.add_right_router(right_x, top_y)
        node.right.add_right(node.right.parent.x, top_y)
        map_h_tree_to_grid(node.right.right,right_x, top_y, length / 2, depth - 1) # 右上
        

    return node

def plot_binary_tree(root):
    """
    绘制生成的二叉树结构。
    :param root: 二叉树的根节点
    """
    def add_edges(node, edges, positions):
        if not node:
            return
        positions[node] = (node.x, node.y)
        if node.left_router:
            positions[node.left_router] = (node.left_router.x, node.left_router.y)
            edges.append(((node.x, node.y), (node.left_router.x, node.left_router.y)))
        if node.right_router:
            positions[node.right_router] = (node.right_router.x, node.right_router.y)
            edges.append(((node.x, node.y), (node.right_router.x, node.right_router.y)))
        if node.left:
            positions[node.left] = (node.left.x, node.left.y)
            edges.append(((node.left_router.x, node.left_router.y), (node.left.x, node.left.y)))
            add_edges(node.left, edges, positions)
        if node.right:
            positions[node.right] = (node.right.x, node.right.y)
            edges.append(((node.right_router.x, node.right_router.y), (node.right.x, node.right.y)))
            add_edges(node.right, edges, positions)

    edges = []
    positions = {}
    add_edges(root, edges, positions)

    plt.figure(figsize=(25, 25))
    for (x1, y1), (x2, y2) in edges:
        plt.plot([x1, x2], [y1, y2], c='black')
    for node, (x, y) in positions.items():
        plt.scatter(x, y, c='blue')
        plt.text(x, y, str(node.address), fontsize=10, ha='center', va='center', color='white',
                 bbox=dict(facecolor='blue', edgecolor='none', boxstyle='circle,pad=0.3'))

    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.show()
    
    

# 示例：生成 H 树网格
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # 初始化参数
    center_x, center_y = 0, 0  # H 树中心
    initial_length = 10  # 初始水平线段长度
    max_depth = 3# 最大递归深度（支持半整数）
    # 存储网格线段和映射关系
    segments = []
    grid_mapping = {}

    # 生成 H 树
    root = map_h_tree_to_grid(RouterQubit(center_x,center_y,0,''),center_x, center_y, initial_length, max_depth)

    # 可视化结果
    plot_binary_tree(root)
    
