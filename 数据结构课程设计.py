import tkinter as tk
# from tkinter import filedialog, scrolledtext
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import filedialog, scrolledtext, ttk
import random 
# 定义全局变量
G = None
path = None
pos = None  # 存储节点位置的全局变量
speed = 1


def handle_user_choice():
    choice = user_choice.get()
    if choice == 'import':  # 导入图文件选项
        import_frame.pack(fill='x', padx=10, pady=5)
        generate_frame.forget()  # 隐藏随机生成图区域
    else:  # 随机生成图选项
        generate_frame.pack(fill='x', padx=10, pady=5)
        import_frame.forget()  # 隐藏导入文件区域

# 定义函数来随机生成图
def generate_graph():
    global G, pos
    node_count = int(node_entry.get())
    edge_count = int(edge_entry.get())
    G = nx.gnm_random_graph(node_count, edge_count, directed=True)
    pos = nx.spring_layout(G)  # 重新计算节点位置
    for (u, v) in G.edges():
        G.edges[u,v]['weight'] = random.randint(1, 10)  # 随机权重
    visualize_graph(G)
    
    
    
# 定义函数
def import_file():
    global G, pos
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        G = nx.DiGraph()
        pos = None  # 重置节点位置
        with open(file_path, 'r') as file:
            for line in file:
                node1, node2, weight = line.strip().split(',')
                G.add_edge(node1, node2, weight=int(weight))
        visualize_graph(G)

def visualize_graph(graph):
    global pos
    if pos is None:
        pos = nx.spring_layout(graph)

    plt.figure(figsize=(8, 6))
    nx.draw(graph, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold', arrows=True)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.title('Directed Graph Visualization')
    plt.show()
    
def visualize_path():
    global G, path, speed, pos
    if not G or not path:
        output_text.insert(tk.END, "请先导入图文件并运行Dijkstra算法找到路径\n")
        return

    plt.ion()  # 开启交互模式

    for i in range(1, len(path)):
        plt.clf()  # 清除当前Figure的当前轴，而不是关闭窗口
        nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold', arrows=True)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        # 绘制到当前节点为止的路径
        nx.draw_networkx_edges(G, pos, edgelist=[(path[j], path[j + 1]) for j in range(i)], edge_color='r', width=2)
        plt.title(f'Shortest Path from {path[0]} to {path[i]}')
        plt.pause(speed)

    plt.ioff()  # 关闭交互模式
    plt.show()
    
    
def dijkstra(start_node, end_node):
    global G, path
    if not G:
        output_text.config(state='normal')  # 允许插入文本
        output_text.insert(tk.END, "请先导入图文件或生成图。\n")
        output_text.config(state='disabled')  # 防止编辑
        return

    try:
        # 检查图中的节点类型，决定是否需要转换用户输入
        if G.nodes():
            sample_node = next(iter(G.nodes()))
            if isinstance(sample_node, int):
                # 尝试将用户输入转换为整数，如果图的节点是整数类型
                start_node = int(start_node)
                end_node = int(end_node)
        
        # 验证节点是否存在于图中
        if start_node not in G.nodes() or end_node not in G.nodes():
            raise ValueError("起始节点或终止节点不在图中。")
        
        path = nx.dijkstra_path(G, start_node, end_node)
        path_length = nx.dijkstra_path_length(G, start_node, end_node)
        output = f"从节点 {start_node} 到节点 {end_node} 的最短路径是: {' -> '.join(map(str, path))}\n"
        output += f"路径长度为: {path_length}\n"
        output_text.config(state='normal')
        output_text.insert(tk.END, output)
        output_text.config(state='disabled')
    except nx.NetworkXNoPath:
        output_text.config(state='normal')
        output_text.insert(tk.END, f"从节点 {start_node} 到节点 {end_node} 不存在路径。\n")
        output_text.config(state='disabled')
    except ValueError as e:
        output_text.config(state='normal')
        output_text.insert(tk.END, f"{e}\n")
        output_text.config(state='disabled')

def update_speed():
    global speed
    try:
        speed = max(1, min(10, int(speed_entry.get())))
    except ValueError:
        speed = 1  # 如果输入无效，重置为默认值
# 创建窗口
window = tk.Tk()
window.title('Dijkstra算法演示系统')
window.geometry('800x600')
# 用户选择区域
choice_frame = tk.Frame(window)
choice_frame.pack(fill='x', padx=10, pady=5)

user_choice = tk.StringVar(value='import')
import_radio = ttk.Radiobutton(choice_frame, text="导入图文件", variable=user_choice, value='import', command=handle_user_choice)
import_radio.pack(side='left', padx=10, pady=5)

generate_radio = ttk.Radiobutton(choice_frame, text="随机生成图", variable=user_choice, value='generate', command=handle_user_choice)
generate_radio.pack(side='left', padx=10, pady=5)
choice_frame2 = tk.Frame(window)
choice_frame2.pack(fill='x', padx=10, pady=5)
store_type = None
generate_radio = ttk.Radiobutton(choice_frame2, text="邻接矩阵", variable=store_type, value='test')
generate_radio.pack(side='left', padx=10, pady=5)
# 导入文件区域
import_frame = tk.Frame(window)
file_button = ttk.Button(import_frame, text='导入图文件', command=import_file)
file_button.pack(fill='x', padx=10, pady=5)

# 随机生成图区域
generate_frame = tk.Frame(window)
node_label = ttk.Label(generate_frame, text="节点数量:")
node_label.pack(side='left', padx=5, pady=5)
node_entry = ttk.Entry(generate_frame)
node_entry.pack(side='left', padx=5, pady=5)

edge_label = ttk.Label(generate_frame, text="路径数量:")
edge_label.pack(side='left', padx=5, pady=5)
edge_entry = ttk.Entry(generate_frame)
edge_entry.pack(side='left', padx=5, pady=5)

generate_button = ttk.Button(generate_frame, text="生成图", command=generate_graph)
generate_button.pack(side='left', padx=10, pady=5)

# Dijkstra 算法区域
dijkstra_frame = tk.Frame(window)
dijkstra_frame.pack(fill='x', padx=10, pady=5)

start_node_label = ttk.Label(dijkstra_frame, text='起始节点:')
start_node_label.pack(side='left', padx=5, pady=5)
start_node_entry = ttk.Entry(dijkstra_frame)
start_node_entry.pack(side='left', padx=5, pady=5)

end_node_label = ttk.Label(dijkstra_frame, text='终止节点:')
end_node_label.pack(side='left', padx=5, pady=5)
end_node_entry = ttk.Entry(dijkstra_frame)
end_node_entry.pack(side='left', padx=5, pady=5)

dijkstra_button = ttk.Button(dijkstra_frame, text='运行Dijkstra算法', command=lambda: dijkstra(start_node_entry.get(), end_node_entry.get()))
dijkstra_button.pack(side='left', padx=10, pady=5)

visualize_button = ttk.Button(dijkstra_frame, text='可视化路径', command=visualize_path)
visualize_button.pack(side='left', padx=10, pady=5)

# 路径展示速度区域
speed_frame = tk.Frame(window)
speed_frame.pack(fill='x', padx=10, pady=5)

speed_label = ttk.Label(speed_frame, text='路径展示速度（1-10）:')
speed_label.pack(side='left', padx=5, pady=5)
speed_entry = ttk.Entry(speed_frame)
speed_entry.pack(side='left', padx=5, pady=5)
confirm_button = ttk.Button(speed_frame, text='确定', command=update_speed)
confirm_button.pack(side='left', padx=10, pady=5)

# 路径输出区域
output_frame = tk.Frame(window)
output_frame.pack(fill='both', expand=True, padx=10, pady=5)

output_text = scrolledtext.ScrolledText(output_frame, state='disabled', height=10)
output_text.pack(fill='both', expand=True, padx=10, pady=5)

# 默认显示导入文件区域
handle_user_choice()

# 进入消息循环
window.mainloop()
