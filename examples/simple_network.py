import json
import panel as pn

from visjs_panel.visjs_panel import VisJS

pn.extension()

nodes = json.dumps([
    {"id": 1, "label": "Node 1"},
    {"id": 2, "label": "Node 2"},
    {"id": 3, "label": "Node 3"},
])
edges = json.dumps([
    {"from": 1, "to": 2},
    {"from": 2, "to": 3},
])

vis = VisJS(nodes=nodes, edges=edges, width=800, height=600)

if __name__ == "__main__":
    pn.serve(vis)

