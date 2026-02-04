from visjs_panel import GraphDetailTool
import panel as pn
import json


nodes = [
        {"id": 1, "label": "Drop an Image File into the graph-widget", "shape":"ellipse", "color": "green"},
        {"id": 2, "label": "Drop a csv File into the graph-widget", "shape":"ellipse", "color": "green"},
    ]
edges = [
    ]


if __name__ == "__main__":
    graph_detail_panel = GraphDetailTool(nodes=json.dumps(nodes), edges=json.dumps(edges))

    pn.serve(graph_detail_panel, threaded=True)