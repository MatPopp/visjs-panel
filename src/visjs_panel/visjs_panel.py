# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 16:00:04 2022

@author: mat87268
"""

import panel as pn
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

        self.detail_markdown = pn.pane.Markdown("## Click on a node to see details", name = "Details")
        self.visualization_markdown = pn.pane.Markdown("## Visualization", name="Visualization")
        self.detail_tabs = pn.Tabs(self.detail_markdown, self.visualization_markdown)
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
        self.detail_markdown.object = f"Details for Node {node_id}"


    def __panel__(self):
        return self._panel

