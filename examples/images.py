import panel as pn
import json
from visjs_panel import VisJS

nodes = [
        {"id": 1, "label": "Würzburg", "shape":"ellipse", "color": "green"},
        {"id": 2, "label": "Festung Marienberg","shape":"ellipse", "color": "blue"},
        {"id": 3, "label": "Residenz", "shape":"ellipse", "color": "blue"},
        {"id": 4, "label": "Käppele", "shape":"ellipse", "color": "blue"},
        {"id": 5, "shape": "image", "size":50, "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Festung_Marienberg_-_W%C3%BCrzburg_-_2013.jpg/1024px-Festung_Marienberg_-_W%C3%BCrzburg_-_2013.jpg"},
        {"id": 6, "shape": "image", "size":50, "image":"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/West_facade_of_the_Wurzburg_Residence_08.jpg/1024px-West_facade_of_the_Wurzburg_Residence_08.jpg"},
        {"id": 7, "shape": "image", "size":50, "image":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Kaeppele_wuerzburg_festungsfoto.jpg/1024px-Kaeppele_wuerzburg_festungsfoto.jpg"},
    ]
edges = [
    {"from": 1, "to": 2, "label": "HasBuilding", "arrows": "to", "color": "black"},
    {"from": 1, "to": 3, "label": "HasBuilding", "arrows": "to", "color": "black"},
    {"from": 1, "to": 4, "label": "HasBuilding", "arrows": "to", "color": "black"},
    {"from": 2, "to": 5, "label": "HasImage", "arrows": "to", "color": "black"},
    {"from": 3, "to": 6, "label": "HasImage", "arrows": "to", "color": "black"},
    {"from": 4, "to": 7, "label": "HasImage", "arrows": "to", "color": "black"},
]


if __name__ == "__main__":
    visjs_panel = VisJS(value="set in constructor", nodes=json.dumps(nodes), edges=json.dumps(edges), width=800,
                        height=600)

    pn.serve(visjs_panel, threaded=True)