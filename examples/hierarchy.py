import panel as pn
import json
from visjs_panel import VisJS

nodes = [
    # Großeltern
    {"id": 10, "label": "Grandfather (Paternal)", "shape": "ellipse", "color": "#a6cee3",
     "x": -200, "y": -200, "fixed": True},
    {"id": 11, "label": "Grandmother (Paternal)", "shape": "ellipse", "color": "#a6cee3",
     "x": -100, "y": -200, "fixed": True},
    {"id": 12, "label": "Grandfather (Maternal)", "shape": "ellipse", "color": "#a6cee3",
     "x": 100, "y": -200, "fixed": True},
    {"id": 13, "label": "Grandmother (Maternal)", "shape": "ellipse", "color": "#a6cee3",
     "x": 200, "y": -200, "fixed": True},

    # Eltern
    {"id": 4, "label": "Father", "shape": "ellipse", "color": "#b2df8a",
     "x": -100, "y": 0, "fixed": True},
    {"id": 5, "label": "Mother", "shape": "ellipse", "color": "#b2df8a",
     "x": 100, "y": 0, "fixed": True},

    # Onkel/Tanten väterlich
    {"id": 7, "label": "Uncle (Paternal)", "shape": "ellipse", "color": "#b2df8a",
     "x": -250, "y": 0, "fixed": True},
    {"id": 8, "label": "Aunt (Paternal)", "shape": "ellipse", "color": "#b2df8a",
     "x": -50, "y": 0, "fixed": True},

    # Onkel/Tanten mütterlich
    {"id": 9, "label": "Uncle (Maternal)", "shape": "ellipse", "color": "#b2df8a",
     "x": 50, "y": 0, "fixed": True},
    {"id": 14, "label": "Aunt (Maternal)", "shape": "ellipse", "color": "#b2df8a",
     "x": 250, "y": 0, "fixed": True},

    # Kinder
    {"id": 1, "label": "Me", "shape": "ellipse", "color": "#fdbf6f",
     "x": -150, "y": 200, "fixed": True},
    {"id": 2, "label": "Brother", "shape": "ellipse", "color": "#fdbf6f",
     "x": -50, "y": 200, "fixed": True},
    {"id": 3, "label": "Sister", "shape": "ellipse", "color": "#fdbf6f",
     "x": 50, "y": 200, "fixed": True},
    {"id": 6, "label": "Younger Brother", "shape": "ellipse", "color": "#fdbf6f",
     "x": 150, "y": 200, "fixed": True},

    # Cousins
    {"id": 15, "label": "Cousin 1 (Paternal)", "shape": "ellipse", "color": "#fdbf6f",
     "x": -300, "y": 200, "fixed": True},
    {"id": 16, "label": "Cousin 2 (Paternal)", "shape": "ellipse", "color": "#fdbf6f",
     "x": -200, "y": 200, "fixed": True},
    {"id": 17, "label": "Cousin 1 (Maternal)", "shape": "ellipse", "color": "#fdbf6f",
     "x": 250, "y": 200, "fixed": True},
    {"id": 18, "label": "Cousin 2 (Maternal)", "shape": "ellipse", "color": "#fdbf6f",
     "x": 350, "y": 200, "fixed": True},
]

edges = [
    {"from": 1, "to": 4, "label": "HasFather", "arrows": "to", "color": "black"},
    {"from": 2, "to": 4, "label": "HasFather", "arrows": "to", "color": "black"},
    {"from": 3, "to": 4, "label": "HasFather", "arrows": "to", "color": "black"},
    {"from": 6, "to": 4, "label": "HasFather", "arrows": "to", "color": "black"},

    {"from": 1, "to": 5, "label": "HasMother", "arrows": "to", "color": "black"},
    {"from": 2, "to": 5, "label": "HasMother", "arrows": "to", "color": "black"},
    {"from": 3, "to": 5, "label": "HasMother", "arrows": "to", "color": "black"},
    {"from": 6, "to": 5, "label": "HasMother", "arrows": "to", "color": "black"},

    {"from": 4, "to": 10, "label": "HasFather", "arrows": "to", "color": "gray"},
    {"from": 4, "to": 11, "label": "HasMother", "arrows": "to", "color": "gray"},

    {"from": 5, "to": 12, "label": "HasFather", "arrows": "to", "color": "gray"},
    {"from": 5, "to": 13, "label": "HasMother", "arrows": "to", "color": "gray"},

    {"from": 7, "to": 10, "label": "HasFather", "arrows": "to", "color": "gray"},
    {"from": 7, "to": 11, "label": "HasMother", "arrows": "to", "color": "gray"},
    {"from": 8, "to": 10, "label": "HasFather", "arrows": "to", "color": "gray"},
    {"from": 8, "to": 11, "label": "HasMother", "arrows": "to", "color": "gray"},

    {"from": 9, "to": 12, "label": "HasFather", "arrows": "to", "color": "gray"},
    {"from": 9, "to": 13, "label": "HasMother", "arrows": "to", "color": "gray"},
    {"from": 14, "to": 12, "label": "HasFather", "arrows": "to", "color": "gray"},
    {"from": 14, "to": 13, "label": "HasMother", "arrows": "to", "color": "gray"},

    {"from": 15, "to": 7, "label": "HasFather", "arrows": "to", "color": "black"},
    {"from": 16, "to": 8, "label": "HasMother", "arrows": "to", "color": "black"},
    {"from": 17, "to": 9, "label": "HasFather", "arrows": "to", "color": "black"},
    {"from": 18, "to": 14, "label": "HasMother", "arrows": "to", "color": "black"},
]

if __name__ == "__main__":
    visjs_panel = VisJS(
        value="set in constructor",
        nodes=json.dumps(nodes),
        edges=json.dumps(edges),
        width=900,
        height=700,
    )
    pn.serve(visjs_panel, threaded=True)