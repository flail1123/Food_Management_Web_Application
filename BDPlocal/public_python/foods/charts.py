import matplotlib.pyplot as plt
import base64
from io import BytesIO
import numpy as np

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x, y):
    plt.switch_backend('AGG')
    objects_list = [f"{i + 1} Jan" for i in range(30)]
    objects = tuple(objects_list)
    y_pos = np.arange(len(objects))
    performance = [np.random.randint(1700, high=2800) for _ in range(30)]
    plt.figure(figsize=(15, 5))
    plt.tight_layout()
    plt.bar(y_pos, performance, align='center', alpha=0.5, width=0.8)
    plt.xticks(y_pos, objects, rotation='vertical')
    plt.ylabel('Calories eaten')
    plt.title('Calories eaten last month')
    graph = get_graph()
    return graph

