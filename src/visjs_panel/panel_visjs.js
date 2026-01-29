// a function that writes the event data into the event queue
function writeEventData(event_name, event_params){
    queue = JSON.parse(data.network_event_queue)
    queue.push({"event_name":event_name, "event_params":event_params})
    data.network_event_queue = JSON.stringify(queue)
    //console.log(event_name + " event added to queue:", data.network_event_queue)
}

// a function that sets options for better network behavior
function setEventFunctions(network){
    network.on('click', function (params) {

        if (params.nodes.length > 0) {
            console.log(params)
            let data = state.nodes.get(params.nodes[0]); // get the data from selected node

            // add the click event to the network_event_queue
            writeEventData("click", params);
            }

    });

    network.on('doubleClick', function (params) {

        if (params.nodes.length == 1) {
            if (network.isCluster(params.nodes[0]) == true) {
              network.openCluster(params.nodes[0]);
              return
            }
            writeEventData("doubleClick", params);

            // Re-enable physics when the user double-clicks a node
            const currentOptions = state.options || {};
            const physicsOptions = Object.assign({}, currentOptions.physics, { enabled: true });
            state.options = Object.assign({}, currentOptions, { physics: physicsOptions });
            network.setOptions({ physics: physicsOptions });
        };

        node=state.nodes.get(params.nodes[0])
        node.fixed = false
        state.nodes.update(node)
    })

    network.on('oncontext', function (params) {
        console.log("oncontext")
        writeEventData("oncontext", params)
    })

    network.on('selectNode', function (params) {
        console.log("selectNode")
        // add the selectNode event to the network_event_queue
        writeEventData("selectNode", params);
    })

    network.on('selectEdge', function (params) {
        console.log("selectEdge")
        // add the selectEdge event to the network_event_queue
        writeEventData("selectEdge", params);
    })

    network.on('hoverNode', function (params) {
        console.log("hoverNode")
        // add the hoverNode event to the network_event_queue
        writeEventData("hoverNode", params);
    })

    network.on('hoverEdge', function (params) {
        console.log("hoverEdge")
        // add the hoverEdge event to the network_event_queue
        writeEventData("hoverEdge", params);
    })

    network.on('zoom', function (params) {
        console.log("zoom")
        // add the zoom event to the network_event_queue
        writeEventData("zoom", params);
    })



    network.on('dragEnd', function (params) {
        if (params.nodes.length>0){
            node = state.nodes.get(params.nodes[0])
            position = network.getPosition(params.nodes[0])   //setting the current position is necessary to prevent snap-back to initial position
            console.log(position)
            node.x=position.x
            node.y=position.y
            node.fixed=true
            state.nodes.update(node)
            data.nodes = JSON.stringify(state.nodes.get())

            // add the dragEnd event to the network_event_queue
            writeEventData("dragEnd", params);
        }

    });


    network.on('dragStart', function (params) {
        if (params.nodes.length>0){

            let node=state.nodes.get(params.nodes[0])
            position = network.getPosition(params.nodes[0])  //setting the current position is necessary to prevent snap-back to initial position
            console.log(position)
            node.x=position.x
            node.y=position.y
            node.fixed=false
            console.log(node)
            state.nodes.update(node)

            // add the dragStart event to the network_event_queue
            writeEventData("dragStart", params);
        }
    });
    network.on("selectNode", function (params) {
        console.log("selectNode")
        data.nodes = JSON.stringify(state.nodes.get())
        data.edges = JSON.stringify(state.edges.get())
         });
    network.on()
}


state.container = network_div   // network div from panel template.
state.nodes = new vis.DataSet(JSON.parse(data.nodes));
state.edges = new vis.DataSet(JSON.parse(data.edges));

// Optionen aus dem Python-Widget lesen (data.options als JSON-String)
let parsedOptions = {};
try {
  if (data.options) {
    parsedOptions = JSON.parse(data.options);
  }
} catch (e) {
  console.warn('Failed to parse options from data.options, using defaults instead.', e);
  parsedOptions = {};
}

// Default-Options, die bei Bedarf mit uebergebenen Optionen gemerged werden
const defaultOptions = {
  manipulation: {
    enabled: true,
    initiallyActive: true,
    addNode: true,
    addEdge: true,
    editEdge: true,
    deleteNode: true,
    deleteEdge: true,
  },
  interaction: { multiselect: true },
  nodes: {
    shape: "dot",
    size: 10,
  },
};

// Einfache Merge-Logik: uebergebene Optionen ueberschreiben Defaults auf oberster Ebene
state.options = Object.assign({}, defaultOptions, parsedOptions);

network_data = {
    nodes: state.nodes,
    edges: state.edges,
};

state.network = new vis.Network(state.container, network_data, state.options);

console.log('state:',state)
console.log('network created, network:', state.network)
setEventFunctions(state.network)

// updating functions
state.update_nodes = function(){
    state.nodes.updateOnly(JSON.parse(data.nodes))
}
