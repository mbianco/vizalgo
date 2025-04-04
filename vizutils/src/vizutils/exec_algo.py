import networkx as nx
from manim import *

def generic_run(selfi, network, **kwargs):
    null_label = kwargs['null_label'] if 'null_label' in kwargs else '-'
    delay = kwargs['delay'] if 'delay' in kwargs else 1
    (Network, layout) = network.get()

    unet = Network.to_undirected()
    network.init_computation()
    finished = False
    time = 0
    while not finished:
        print(f'Iteration {time}')
        if time == 0:
            selfi.G = Graph.from_networkx(Network, layout=layout, labels={i : Network.nodes[i]['weight']['value'] for i in Network}, 
                                    edge_config={(u,v): {'stroke_color': (WHITE if d['weight']['carry'] != null_label else d['weight']['color']),
                                                         'stroke_width': (6 if d['weight']['carry'] != null_label else 3)} 
                                                         for u, v, d in Network.edges(data = True)},
                                    vertex_config={u: {'fill_color': (WHITE if Network.nodes[u]['weight']['value'] != null_label else BLACK),
                                                       'stroke_width': 3, 'stroke_color': Network.nodes[u]['weight']['color']}
                                                   for u in Network.nodes})
            selfi.play(Create(selfi.G))
            counter = Text(str(time)).to_edge(UL)
            selfi.add(counter)
            try:
                network.additional_items_to_draw(selfi)
            except Exception as e:
                print("Nothing to add:", e)
        else:
            selfi.wait(delay)
            G1 = Graph.from_networkx(Network, layout=layout, labels={i : Network.nodes[i]['weight']['value'] for i in Network}, 
                                    edge_config={(u,v): {'stroke_color': (WHITE if d['weight']['carry'] != null_label else d['weight']['color']),
                                                         'stroke_width': (6 if d['weight']['carry'] != null_label else 3)} 
                                                         for u, v, d in Network.edges(data = True)},
                                    vertex_config={u: {'fill_color': (WHITE if Network.nodes[u]['weight']['value'] != null_label else BLACK),
                                                       'stroke_width': 3, 'stroke_color': Network.nodes[u]['weight']['color']}
                                                   for u in Network.nodes})

            new_texts_from = {(u, v): Text(str(Network[u][v]['weight']['carry']), color=RED, font_size=32)
                        for u, v, d in Network.edges(data=True) if d['weight']['carry'] != null_label}
            new_texts_to = {(u, v): Text(str(Network[u][v]['weight']['carry']), color=RED, font_size=32)
                        for u, v, d in Network.edges(data=True) if d['weight']['carry'] != null_label}
            try:
                network.additional_items_to_draw(selfi)
            except Exception as e:
                print("Nothing to add:", e)

            selfi.play(Transform(selfi.G, G1), *[Transform(new_texts_from[(u, v)].move_to(selfi.G[u]), new_texts_to[(u, v)].move_to(selfi.G[v])) 
                                           for u, v, d in Network.edges(data=True) if d['weight']['carry'] != null_label], 
                        path_arc = 70 * DEGREES, run_time=1.5*delay)
            selfi.play(Transform(counter, Text(str(time)).to_edge(UL)) ,*[FadeOut(new_texts_from[(u, v)]) for u, v, d in Network.edges(data=True) if d['weight']['carry'] != null_label], run_time=1.5*delay)
        finished = not network.compute_iteration()
        time = time+1
    selfi.wait(delay)