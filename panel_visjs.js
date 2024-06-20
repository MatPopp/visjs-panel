

// a function that sets options for better network behavior
function setEventFunctions(network){
    network.on('click', function (params) {

        if (params.nodes.length > 0) {
            console.log(params)
            let data = state.nodes.get(params.nodes[0]); // get the data from selected node
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
        }
    });

    network.on('doubleClick', function (params) {

        if (params.nodes.length == 1) {
            if (network.isCluster(params.nodes[0]) == true) {
              network.openCluster(params.nodes[0]);
              return
            }
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

