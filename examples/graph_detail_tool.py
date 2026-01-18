import json
import panel as pn

from visjs_panel.visjs_panel import GraphDetailTool

pn.extension()

nodes = json.dumps([
    {"id": 1, "label": "Alpha"},
    {"id": 2, "label": "Beta"},
    {"id": 3, "label": "Gamma"},
])
edges = json.dumps([
    {"from": 1, "to": 2},
    {"from": 2, "to": 3},
    {"from": 3, "to": 1},
])

tool = GraphDetailTool(nodes=nodes, edges=edges)

if __name__ == "__main__":
    pn.serve(tool)

