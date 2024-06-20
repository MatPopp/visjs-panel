# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 16:00:04 2022

@author: mat87268
"""

import panel as pn
#from pprint import pprint
import json
import time
import numpy as np
#from matplotlib import cm
#from matplotlib.colors import rgb2hex

#import networkx as nx

from panel.reactive import ReactiveHTML
import param

#pn.extension(css_files = ['https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.9/dist/dist/vis-network.min.css'])

### imoprt javascript

# open text file in read mode
with open("panel_visjs.js", "r") as file:
    # read whole file to a string
    js_string = file.read()


class VisJS(ReactiveHTML):
    value = param.String(default='no response so far')
    nodes = param.String(default="[]")
    edges = param.String(default="[]")

    _template = """ 
   <div id="network_div" style="position:absolute;width:800px;height:600px;
   background-color:#ffffff;border:1px solid #000000;" onclick="${_on_div_clicked}"> </div>
    """

    # By declaring an _extension_name the component should be loaded explicitly with pn.extension('material-components')
    #_extension_name = 'VisJS'

    _scripts = {
        'render': js_string,
        'nodes': "state.update_nodes()",
        'edges': "console.log('edges changed:',data.edges)"
    }
    __javascript__ = [
        #"https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"  ## external link
        'https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.9/dist/vis-network.min.js'
    ]

    def __init__(self, nodes = None, edges = None, value = None, **params):
        self.nodes = nodes
        self.edges = edges
        print("nodes: ", self.nodes)
        print("edges: ", self.edges)
        super().__init__(**params)
        self.param.watch(self.print_nodes, "nodes")
        self.param.watch(self.print_edges, "edges")

    def print_nodes(self, event):
        print("nodes: ", self.nodes)

    def print_edges(self, event):
        print("nodes: ", self.edges)

    def _on_div_clicked(self, event):
        print("div clicked", event)

def example_hierarchy():
    ## simple family tree

    nodes = [
        {"id": 1, "label": "Me", "shape":"ellipse", "color": "#e04141"},
        {"id": 2, "label": "Brother","shape":"ellipse", "color": "#e09c41"},
        {"id": 3, "label": "Sister", "shape":"ellipse", "color": "#e0df41"},
        {"id": 4, "label": "Father", "shape":"ellipse", "color": "#7be041"},
        {"id": 5, "label": "Mother", "shape":"ellipse", "color": "#41e0c9"},

    ]
    edges = [
        {"from": 1, "to": 4, "label": "HasFather", "arrows": "to", "color": "black"},
        {"from": 2, "to": 4, "label": "HasFather", "arrows": "to", "color": "black"},
        {"from": 3, "to": 4, "label": "HasFather", "arrows": "to", "color": "black"},
        {"from": 1, "to": 5, "label": "HasMother", "arrows": "to", "color": "black"},
        {"from": 2, "to": 5, "label": "HasMother", "arrows": "to", "color": "black"},
        {"from": 3, "to": 5, "label": "HasMother", "arrows": "to", "color": "black"}
    ]

    visjs_panel = VisJS(value="set in constructor", nodes=json.dumps(nodes), edges=json.dumps(edges), width=800,
                        height=600)

    pn.serve(visjs_panel, threaded=True)

def example_images():
    ## simple family tree

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

    visjs_panel = VisJS(value="set in constructor", nodes=json.dumps(nodes), edges=json.dumps(edges), width=800,
                        height=600)

    pn.serve(visjs_panel, threaded=True)

def example_rotating_circles():
    ## create some dummy data
    import numpy as np
    import time

    last_t = time.time()
    phi_0 = 0
    r = 100
    phi_1 = 2 * np.pi / 5
    phi_2 = 2 * 2 * np.pi / 5
    phi_3 = 3 * 2 * np.pi / 5
    phi_4 = 4 * 2 * np.pi / 5

    nodes = [
        {"id": 1, "label": "Node 1", "color": "#e04141", "x": r * np.cos(phi_0), "y": r * np.sin(phi_0), "fixed": True},
        {"id": 2, "label": "Node 2", "color": "#e09c41", "x": r * np.cos(phi_0 + phi_1), "y": r * np.sin(phi_0 + phi_1),
         "fixed": True},
        {"id": 3, "label": "Node 3", "color": "#e0df41", "x": r * np.cos(phi_0 + phi_2), "y": r * np.sin(phi_0 + phi_2),
         "fixed": True},
        {"id": 4, "label": "Node 4", "color": "#7be041", "x": r * np.cos(phi_0 + phi_3), "y": r * np.sin(phi_0 + phi_3),
         "fixed": True},
        {"id": 5, "label": "Node 5", "color": "#41e0c9", "x": r * np.cos(phi_0 + phi_4), "y": r * np.sin(phi_0 + phi_4),
         "fixed": True},

        {"id": 6, "label": "Node 6", "color": "#e04141"},
        {"id": 7, "label": "Node 7", "color": "#e09c41"},
        {"id": 8, "label": "Node 8", "color": "#e0df41"},
        {"id": 9, "label": "Node 9", "color": "#7be041"},
        {"id": 10, "label": "Node 10", "color": "#41e0c9"}
    ]

    edges = [
        {"from": 1, "to": 2},
        {"from": 2, "to": 3},
        {"from": 3, "to": 4},
        {"from": 4, "to": 5},
        {"from": 5, "to": 1},
        {"from": 1, "to": 6},
        {"from": 2, "to": 7},
        {"from": 3, "to": 8},
        {"from": 4, "to": 9},
        {"from": 5, "to": 10}
    ]

    visjs_panel = VisJS(value="set in constructor", nodes=json.dumps(nodes), edges=json.dumps(edges), width=800,
                        height=600)
    vel_slider = pn.widgets.FloatSlider(name='Velocity', start=-20, end=20, value=1, width=600)
    radius_slider = pn.widgets.FloatSlider(name='Radius', start=0, end=500, value=r, width=600)

    col = pn.Column(visjs_panel, vel_slider, radius_slider)
    pn.serve(col, threaded=True)

    while True:
        phi_0 += vel_slider.value * (time.time() - last_t)
        last_t = time.time()
        r = radius_slider.value

        nodes = [
            {"id": 1, "label": "Node 1", "color": "#e04141", "x": r * np.cos(phi_0), "y": r * np.sin(phi_0),
             "fixed": True},
            {"id": 2, "label": "Node 2", "color": "#e09c41", "x": r * np.cos(phi_0 + phi_1),
             "y": r * np.sin(phi_0 + phi_1), "fixed": True},
            {"id": 3, "label": "Node 3", "color": "#e0df41", "x": r * np.cos(phi_0 + phi_2),
             "y": r * np.sin(phi_0 + phi_2), "fixed": True},
            {"id": 4, "label": "Node 4", "color": "#7be041", "x": r * np.cos(phi_0 + phi_3),
             "y": r * np.sin(phi_0 + phi_3), "fixed": True},
            {"id": 5, "label": "Node 5", "color": "#41e0c9", "x": r * np.cos(phi_0 + phi_4),
             "y": r * np.sin(phi_0 + phi_4), "fixed": True},

            {"id": 6, "label": "Node 6", "color": "#e04141"},
            {"id": 7, "label": "Node 7", "color": "#e09c41"},
            {"id": 8, "label": "Node 8", "color": "#e0df41"},
            {"id": 9, "label": "Node 9", "color": "#7be041"},
            {"id": 10, "label": "Node 10", "color": "#41e0c9"}
        ]
        visjs_panel.nodes = json.dumps(nodes)
        time.sleep(0.01)

if __name__ == '__main__':

    example_hierarchy()
    example_images()
    example_rotating_circles()