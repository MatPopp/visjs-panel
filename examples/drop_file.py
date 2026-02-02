import panel as pn
import json
from visjs_panel import VisJS

nodes = [
        {"id": 1, "label": "Drop an Image File into the graph-widget", "shape":"ellipse", "color": "green"},
    ]
edges = [
    ]


if __name__ == "__main__":
    visjs_panel = VisJS(value="set in constructor", nodes=json.dumps(nodes), edges=json.dumps(edges), width=800,
                        height=600)

    pn.serve(visjs_panel, threaded=True)