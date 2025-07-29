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

    network.on('doubleClick', function (params) {

        if (params.nodes.length == 1) {
            if (network.isCluster(params.nodes[0]) == true) {
              network.openCluster(params.nodes[0]);
              return
            }
            writeEventData("doubleClick", params);
        };

        node=state.nodes.get(params.nodes[0])
        node.fixed = false
        state.nodes.update(node)
    })

    network.on("selectNode", function (params) {
        console.log("selectNode")
        data.nodes = JSON.stringify(state.nodes.get())
        data.edges = JSON.stringify(state.edges.get())
         });
}


state.container = network_div   // network div from panel template.
state.nodes = new vis.DataSet(JSON.parse(data.nodes));
state.edges = new vis.DataSet(JSON.parse(data.edges));



console.log(state.nodes, state.edges)
// create a network
network_data = {
    nodes: state.nodes,
    edges: state.edges,
};

state.options = {
    manipulation: {
      enabled: true,
      initiallyActive: true,
      addNode: true,
      addEdge: true,
      editEdge: true,
      deleteNode: true,
      deleteEdge: true,
    },
    interaction:{multiselect:true},
    nodes:{shape:"dot",
      size:10,
    }
  };

state.network = new vis.Network(state.container, network_data, state.options);

console.log('state:',state)
console.log('network created, network:', state.network)
setEventFunctions(state.network)

// updating functions
state.update_nodes = function(){
    state.nodes.updateOnly(JSON.parse(data.nodes))
}

