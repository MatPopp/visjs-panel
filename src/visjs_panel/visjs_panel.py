# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 16:00:04 2022

@author: mat87268
"""

import panel as pn
from visjs_panel.utils import data_url_to_bytes
#from pprint import pprint
import json

from panel.reactive import ReactiveHTML
import param

#pn.extension(css_files = ['https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.9/dist/dist/vis-network.min.css'])

### import javascript from package resources
try:
    from importlib.resources import files as _pkg_files  # Python 3.9+
except ImportError:  # Python <3.9 fallback
    from importlib_resources import files as _pkg_files  # type: ignore

# resolve packaged path to panel_visjs.js regardless of CWD
_js_path = _pkg_files(__package__).joinpath("panel_visjs.js")
js_string = _js_path.read_text(encoding="utf-8")


class VisJS(ReactiveHTML):
    value = param.String(default='no response so far')
    nodes = param.String(default="[]")
    edges = param.String(default="[]")
    network_event_queue = param.String(default="[]")
    # Neue Eigenschaft: options als JSON-String, der ins JS uebergeben wird
    options = param.String(default="{}")

    #
    _template = """ 
   <div id="network_div" style="position:absolute;width:800px;height:600px;
   background-color:#ffffff;border:1px solid #000000;" onclick="${_on_div_clicked}"> 
   </div>
    """

    # By declaring an _extension_name the component should be loaded explicitly with pn.extension('material-components')
    # _extension_name = 'VisJS'

    _scripts = {
        'render': js_string,
        'nodes': "state.update_nodes()",
        'edges': "console.log('edges changed:',data.edges)"
    }
    __javascript__ = [
        # "https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"  ## external link
        'https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.9/dist/vis-network.min.js'
    ]

    def __init__(self, nodes=None, edges=None, value=None,
                 network_event_callback=None,
                 file_drop_callback: callable = None,
                 options=None,
                 **params):
        # Eingehende Argumente in die param-Properties schreiben
        if nodes is not None:
            self.nodes = nodes
        if edges is not None:
            self.edges = edges
        if value is not None:
            self.value = value
        if options is not None:
            self.options = options

        self.file_drop_callback = self.default_file_drop_callback
        if file_drop_callback is not None:
            self.file_drop_callback = file_drop_callback

        self.network_event_callback = network_event_callback

        print("nodes: ", self.nodes)
        print("edges: ", self.edges)
        print("options: ", self.options)
        super().__init__(**params)
        self.param.watch(self.print_nodes, "nodes")
        self.param.watch(self.print_edges, "edges")
        self.param.watch(self.network_event_handler, "network_event_queue")

    def print_nodes(self, event):
        print("nodes: ", self.nodes)

    def print_edges(self, event):
        print("nodes: ", self.edges)

    def network_event_handler(self, event):
        """
        Callback for visjs-network events.
        """
        print("network_event_queue: ", self.network_event_queue)

        while len(json.loads(self.network_event_queue)) > 0:
            network_event_queue_list = json.loads(self.network_event_queue)
            event_json = network_event_queue_list.pop(0)
            event_name = event_json.get("event_name", None)
            event_params = event_json.get("event_params", None)
            if event_name and event_params:
                self.handle_network_event(event_name, event_params)
            self.network_event_queue = json.dumps(network_event_queue_list)

    def _on_div_clicked(self, event):
        pass
        # print("div clicked", event)

    def expand_node(self, node_id):
        print("not implemented so far, expand node:", node_id)

    def handle_network_event(self, event_name, event_params_dict):
        """
        Handle network events from the visjs-network.
        """
        if self.network_event_callback is not None:
            self.network_event_callback(event_name, event_params_dict)
        if event_name == "dragStart":
            print("Node drag started:", event_params_dict)
        if event_name == "dragEnd":
            print("Node drag ended:", event_params_dict)
        if event_name == "click":
            print("Node clicked:", event_params_dict)
        if event_name == "doubleClick":
            print("Node double clicked:", event_params_dict)
            node_ids = event_params_dict.get("nodes", None)
            if node_ids:
                for node_id in node_ids:
                    self.expand_node(node_id)
        if event_name == "oncontext":
            print("Node has been rightclicked")

        if event_name == "fileDrop":
            print("File dropped event:", event_params_dict)
            self.file_drop_callback(event_params_dict)



    def default_file_drop_callback(self, event):
        """
        Default callback for file drop events on the visjs-network.
        """
        print("File dropped:", event)
        files = event.get("files", None)
        if files:
            for file in files:
                print("Dropped file:", file)
                if "content" in file:
                    if file["content"].startswith("data:image"):
                        new_nodes = json.loads(self.nodes)
                        new_nodes.append({
                            "id": file["name"],
                            "label": file["name"],
                            "shape": "image",
                            "image": file["content"],
                            "data": file["content"],
                            "size": 30,
                            "x": event.get("x", None),
                            "y": event.get("y", None),
                        })

                        print("Adding new node for dropped image file:", file["name"])
                        self.nodes = json.dumps(new_nodes)  # Trigger update

                    elif file["content"].startswith("data"):
                        new_nodes = json.loads(self.nodes)
                        new_nodes.append({
                            "id": file["name"],
                            "label": file["name"],
                            "shape": "ellipse",
                            "data": file["content"],
                            "size": 30,
                            "x": event.get("x", None),
                            "y": event.get("y", None),
                        })
                        print("Adding new node for dropped data file:", file["name"])
                        self.nodes = json.dumps(new_nodes)  # Trigger update







class GraphDetailTool:
    def __init__(self, nodes, edges):

        self.nodes = nodes
        self.edges = edges
        self.build_panel()


    def build_panel(self):
        self.visjs_panel = VisJS(value="set in constructor",
                                 nodes=self.nodes,
                                 edges=self.edges,
                                 width=800,
                                 height=600,
                                 network_event_callback=self.network_event_callback,
                                 )


        self.visualizations_col = pn.Column(pn.pane.Markdown("## Click on node for Visualizations"),
                                            name="Visualization")
        self.detail_col= pn.Column(pn.pane.Markdown("## Click on a node to see details"), name = "Details")
        self.detail_tabs = pn.Tabs(self.visualizations_col, self.detail_col, )
        self._panel = pn.Row(self.visjs_panel, self.detail_tabs)

    def network_event_callback(self, event_name, event_params_dict):
        """
        Callback for network events from the visjs-network.
        """
        print("Network event callback:", event_params_dict)
        if event_name == "click":
            self.click_callback(event_params_dict)


    def click_callback(self, event):
        """
        Callback for click events on the visjs-network.
        """
        print("Node clicked:", event)
        node_ids = event.get("nodes", None)
        if node_ids:
            for node_id in node_ids:
                self.show_node_details(node_id)

    def show_node_details(self, node_id):
        """
        Show details for a clicked node.
        """
        print("Showing details for node:", node_id)
        self.detail_col.clear()
        nodes_list = json.loads(self.visjs_panel.nodes)
        current_node_dict = [node for node in nodes_list if node["id"]==node_id][0]
        self.detail_col.append(pn.pane.Markdown(f"### Node ID: {current_node_dict['id']}"))
       # self.detail_col.append(pn.widgets.JSONEditor(value= current_node_dict))
        self.detail_col.append(pn.pane.Markdown(json.dumps(current_node_dict)))
        print("Current node dict:", current_node_dict)

        ## re-build visualizations column
        self.visualizations_col.clear()
        if "image" in current_node_dict:

            self.visualizations_col.append(pn.pane.Image(data_url_to_bytes(current_node_dict["image"])))


    def __panel__(self):
        return self._panel

