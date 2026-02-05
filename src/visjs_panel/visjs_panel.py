# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 16:00:04 2022

@author: mat87268
"""

import panel as pn
from visjs_panel.utils import data_url_to_bytes
#from pprint import pprint
import json
import pandas as pd
from io import StringIO
# Plotly lokal importieren, um Abhängigkeit nur bei Bedarf zu ziehen
import plotly.express as px

from panel.custom import AnyWidgetComponent
import param

pn.extension("plotly", "jsoneditor")

#pn.extension(css_files = ['https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.9/dist/dist/vis-network.min.css'])

### import javascript from package resources
try:
    from importlib.resources import files as _pkg_files  # Python 3.9+
except ImportError:  # Python <3.9 fallback
    from importlib_resources import files as _pkg_files  # type: ignore

# resolve packaged path to panel_visjs.js regardless of CWD
_js_path = _pkg_files(__package__).joinpath("panel_visjs.js")
js_string = _js_path.read_text(encoding="utf-8")


class VisJS(AnyWidgetComponent):
    value = param.String(default='no response so far')
    nodes = param.String(default="[]")
    edges = param.String(default="[]")
    network_event_queue = param.String(default="[]")
    manipulation_state = param.String(default="disableEditMode") # "addNodeMode", "addEdgeMode"

    # Neue Eigenschaft: options als JSON-String, der ins JS uebergeben wird
    options = param.String(default="{}")

    _esm = js_string

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

        #print("nodes: ", self.nodes)
        #print("edges: ", self.edges)
        #print("options: ", self.options)
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
                #print("Dropped file:", file)
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


    def disable_edit_mode(self):
        self.manipulation_state = "" # toggle to re-trigger
        self.manipulation_state = "disableEditMode"

    def add_node_mode(self):
        self.manipulation_state = "" # toggle to re-trigger
        self.manipulation_state = "addNodeMode"

    def add_edge_mode(self):
        self.manipulation_state = "" # toggle to re-trigger
        self.manipulation_state = "addEdgeMode"







class GraphDetailTool:
    def __init__(self, nodes, edges):

        self.nodes = nodes
        self.edges = edges
        self.build_panel()

        self.current_node_jsoneditor = None


    def build_panel(self):

        self.disable_edit_button = pn.widgets.Button(name="Disable Edit", button_type="primary")
        self.disable_edit_button.on_click(lambda event: self.visjs_panel.disable_edit_mode())
        self.add_node_button = pn.widgets.Button(name="Add Node", button_type="success")
        self.add_node_button.on_click(lambda event: self.visjs_panel.add_node_mode())
        self.add_edge_button = pn.widgets.Button(name="Add Edge", button_type="success")
        self.add_edge_button.on_click(lambda event: self.visjs_panel.add_edge_mode())
        self.edit_row = pn.Row(
            self.disable_edit_button,
            self.add_node_button,
            self.add_edge_button,
        )

        self.visjs_panel = VisJS(value="set in constructor",
                                 nodes=self.nodes,
                                 edges=self.edges,
                                 width=800,
                                 height=600,
                                 network_event_callback=self.network_event_callback,
                                 )
        self.graph_col = pn.Column(self.edit_row, self.visjs_panel)

        self.visualizations_col = pn.Column(pn.pane.Markdown("## Click on node for Visualizations"),
                                            name="Visualization")
        self.detail_col= pn.Column(pn.pane.Markdown("## Click on a node to see details"), name = "Details")

        self.detail_tabs = pn.Tabs(self.visualizations_col, self.detail_col, )

        self._panel = pn.Row(self.graph_col, self.detail_tabs)

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

    def update_node_callback(self, event):
        """
        Callback for node updates from the JSON editor.
        """
        print("Node updated:", event)
        new_node_dict = event.new
        self.update_node(new_node_dict)

    def update_node(self, new_node_dict):
        """
        Update a node in the visjs-panel.
        """
        print("Updating node:", new_node_dict)
        nodes_list = json.loads(self.visjs_panel.nodes)
        for i, node in enumerate(nodes_list):
            if node["id"] == new_node_dict["id"]:
                nodes_list[i] = new_node_dict
                break
        self.visjs_panel.nodes = json.dumps(nodes_list)

    def show_node_details(self, node_id):
        """
        Show details for a clicked node.
        """

        print("Showing details for node:", node_id)
        self.detail_col.clear()
        nodes_list = json.loads(self.visjs_panel.nodes)
        current_node_dict = [node for node in nodes_list if node["id"]==node_id][0]
        self.detail_col.append(pn.pane.Markdown(f"### Node ID: {current_node_dict['id']}"))

        self.current_node_jsoneditor = pn.widgets.JSONEditor(value= current_node_dict)
        self.current_node_jsoneditor.param.watch(self.update_node_callback, "value")

        self.detail_col.append(self.current_node_jsoneditor)
        print("Current node dict:", current_node_dict)

        ## re-build visualizations column
        self.visualizations_col.clear()

        # Images
        if "image" in current_node_dict:
            self.visualizations_col.append(pn.pane.Image(data_url_to_bytes(current_node_dict["image"])))

        # .csv files
        if "data" in current_node_dict:
            if (
                    current_node_dict["data"].startswith("data:text/csv")
                    or current_node_dict["data"].startswith("data:application/vnd.ms-excel")
            ):
                csv_bytes = data_url_to_bytes(current_node_dict["data"])
                csv_str = csv_bytes.decode("utf-8")

                # Delimiter automatisch erkennen
                df = pd.read_csv(
                    StringIO(csv_str),
                    sep=None,
                    engine="python",
                )

                self.visualizations_col.append(pn.pane.Markdown("### CSV Data Preview"))
                self.visualizations_col.append(
                    pn.widgets.DataFrame(df, width=600, height=300)
                )

                # Spaltenlisten bestimmen
                all_cols = list(df.columns)
                numeric_cols = list(df.select_dtypes(include="number").columns)

                if len(numeric_cols) == 0:
                    self.visualizations_col.append(
                        pn.pane.Markdown(
                            "*(Keine numerischen Spalten für Plotly-Plot gefunden.)*"
                        )
                    )
                    return

                # Default-Auswahl
                default_x = all_cols[0]
                default_y = numeric_cols[0]

                x_select = pn.widgets.Select(
                    name="x-Achse",
                    options=all_cols,
                    value=default_x,
                )
                y_select = pn.widgets.Select(
                    name="y-Achse",
                    options=numeric_cols,
                    value=default_y,
                )

                def make_figure(x_col, y_col):
                    # Falls y\-Spalte nicht numerisch ist, leer zurückgeben
                    if y_col not in df.select_dtypes(include="number").columns:
                        return pn.pane.Markdown(
                            "*(Gewählte y-Spalte ist nicht numerisch.)*"
                        )
                    fig = px.line(
                        df,
                        x=x_col,
                        y=y_col,
                        title=f"Plot von '{y_col}' gegen '{x_col}'",
                    )
                    return pn.pane.Plotly(fig, config={"responsive": True})

                plot_pane = pn.bind(make_figure, x_col=x_select, y_col=y_select)

                self.visualizations_col.append(pn.pane.Markdown("### CSV Plot"))
                self.visualizations_col.append(
                    pn.Column(
                        pn.Row(x_select, y_select, width=250),
                        plot_pane,
                    )
                )
            #text files
            print("Checking for text data in node...")
            if current_node_dict["data"].startswith("data:text/plain"):
                text_bytes = data_url_to_bytes(current_node_dict["data"])
                text_str = text_bytes.decode("utf-8")
                self.visualizations_col.append(pn.pane.Markdown("### Text Preview"))
                self.visualizations_col.append(
                    pn.pane.Markdown(f"```\n{text_str}\n```")
                )

            #pdf files
            # todo: find out why this can take a minute for 6MB pdf
            print("Checking for pdf data in node...")
            print("start of data:", current_node_dict["data"][:50])
            if current_node_dict["data"].startswith("data:application/pdf"):
                pdf_bytes = data_url_to_bytes(current_node_dict["data"])
                self.visualizations_col.append(pn.pane.Markdown("### PDF Preview"))
                self.visualizations_col.append(
                    pn.pane.PDF(pdf_bytes, width=600, height=800)
                )

    def __panel__(self):
        return self._panel

