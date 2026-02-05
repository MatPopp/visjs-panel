// AnyWidget ESM module for VisJS Panel
// Load vis.js library dynamically
async function loadVisJS() {
  if (typeof vis !== 'undefined') {
    return vis;
  }

  // Load vis-network from CDN
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.9/dist/vis-network.min.js';
    script.onload = () => resolve(window.vis);
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

export async function render({ model, el }) {
  // Wait for vis.js to load
  const vis = await loadVisJS();

  // Create container div
  const container = document.createElement('div');
  container.style.position = 'absolute';
  container.style.width = '800px';
  container.style.height = '600px';
  container.style.backgroundColor = '#ffffff';
  container.style.border = '1px solid #000000';
  el.appendChild(container);

  // Initialize state
  const state = {
    container: container,
    nodes: new vis.DataSet(JSON.parse(model.get('nodes'))),
    edges: new vis.DataSet(JSON.parse(model.get('edges'))),
    network: null,
    options: {}
  };

  // Function to send event data to Python via Panel's parameter mechanism
  function sendEventToPython(event_name, event_params) {
    const event_data = JSON.stringify({
      "event_name": event_name,
      "event_params": event_params,
      "timestamp": Date.now()  // Add timestamp to ensure parameter change is detected
    });
    model.set('_event_data', event_data);
    model.save_changes();
  }

  // Function to set event listeners on the network
  function setEventFunctions(network) {
    network.on('click', function (params) {
      if (params.nodes.length > 0) {
        console.log(params);
        let data = state.nodes.get(params.nodes[0]);
        sendEventToPython("click", params);
      }
    });

    network.on('doubleClick', function (params) {
      if (params.nodes.length == 1) {
        if (network.isCluster(params.nodes[0]) == true) {
          network.openCluster(params.nodes[0]);
          return;
        }
        sendEventToPython("doubleClick", params);

        // Re-enable physics when the user double-clicks a node
        const currentOptions = state.options || {};
        const physicsOptions = Object.assign({}, currentOptions.physics, { enabled: true });
        state.options = Object.assign({}, currentOptions, { physics: physicsOptions });
        network.setOptions({ physics: physicsOptions });
      }

      const node = state.nodes.get(params.nodes[0]);
      node.fixed = false;
      state.nodes.update(node);
    });

    network.on('oncontext', function (params) {
      console.log("oncontext");
      sendEventToPython("oncontext", params);
    });

    network.on('selectNode', function (params) {
      console.log("selectNode");
      sendEventToPython("selectNode", params);
    });

    network.on('selectEdge', function (params) {
      console.log("selectEdge");
      sendEventToPython("selectEdge", params);
    });

    network.on('hoverNode', function (params) {
      console.log("hoverNode");
      sendEventToPython("hoverNode", params);
    });

    network.on('hoverEdge', function (params) {
      console.log("hoverEdge");
      sendEventToPython("hoverEdge", params);
    });

    network.on('zoom', function (params) {
      console.log("zoom");
      sendEventToPython("zoom", params);
    });

    network.on('dragEnd', function (params) {
      if (params.nodes.length > 0) {
        // Update each node in dataset
        for (let node of state.nodes.get()) {
          console.log("node", node);

          const pos = network.getPosition(node.id);
          node.x = pos.x;
          node.y = pos.y;

          if (node.id === params.nodes[0]) {
            console.log("fixing node:", node.id);
            node.fixed = true;
          }
          state.nodes.update(node);
        }

        // Write complete node state back to model
        model.set('nodes', JSON.stringify(state.nodes.get()));
        model.save_changes();

        // Send event to Python
        sendEventToPython("dragEnd", params);
      }
    });

    network.on('dragStart', function (params) {
      if (params.nodes.length > 0) {
        let node = state.nodes.get(params.nodes[0]);
        const position = network.getPosition(params.nodes[0]);
        console.log(position);
        node.x = position.x;
        node.y = position.y;
        node.fixed = false;
        console.log(node);
        state.nodes.update(node);

        sendEventToPython("dragStart", params);
      }
    });

    network.on("selectNode", function (params) {
      console.log("selectNode");
      model.set('nodes', JSON.stringify(state.nodes.get()));
      model.set('edges', JSON.stringify(state.edges.get()));
      model.save_changes();
    });
  }

  // Drag & Drop support
  function handleDrop(dropEvent) {
    dropEvent.preventDefault();
    const files = dropEvent.dataTransfer.files;
    console.log('Files dropped:', files);

    let drop_event = state.network.DOMtoCanvas({
      x: dropEvent.clientX,
      y: dropEvent.clientY
    });
    drop_event.files = [];

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const reader = new FileReader();
      reader.onload = function (event) {
        const fileContent = event.target.result;
        console.log('File content:', fileContent);
        drop_event.files.push({ name: file.name, content: fileContent });
      };
      reader.readAsDataURL(file);

      if (i === files.length - 1) {
        reader.onloadend = function () {
          console.log('All files processed:', drop_event.files);
          sendEventToPython("fileDrop", drop_event);
        };
      }
    }
  }

  function addContainerEventListeners(container) {
    container.addEventListener('dragenter', function (e) {
      e.preventDefault();
      container.style.border = '1px solid black';
    }, false);

    container.addEventListener('dragleave', function (e) {
      container.style.border = '1px solid lightgray';
    }, false);

    container.addEventListener('drop', function (e) {
      e.preventDefault();
      handleDrop(e);
    }, false);

    container.addEventListener('dragover', function (e) {
      e.preventDefault();
    }, false);
  }

  addContainerEventListeners(state.container);

  // Parse options from model
  let parsedOptions = {};
  try {
    const optionsStr = model.get('options');
    if (optionsStr) {
      parsedOptions = JSON.parse(optionsStr);
    }
  } catch (e) {
    console.warn('Failed to parse options from model, using defaults instead.', e);
    parsedOptions = {};
  }

  // Default options
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

  // Merge options
  state.options = Object.assign({}, defaultOptions, parsedOptions);

  // Create network
  const network_data = {
    nodes: state.nodes,
    edges: state.edges,
  };

  state.network = new vis.Network(state.container, network_data, state.options);

  console.log('state:', state);
  console.log('network created, network:', state.network);
  setEventFunctions(state.network);

  // Update functions for when model changes
  function update_nodes() {
    state.nodes.update(JSON.parse(model.get('nodes')));
  }

  function update_edges() {
    state.edges.update(JSON.parse(model.get('edges')));
  }

  function update_manipulation_state() {
    const manipulation_state = model.get('manipulation_state');
    console.log("update_manipulation_state:", manipulation_state);

    if (manipulation_state === "disableEditMode") {
      console.log("disableEditMode");
      state.network.disableManipulation();
    }
    if (manipulation_state === "addNodeMode") {
      console.log("addNodeMode");
      state.network.addNodeMode();
    }
    if (manipulation_state === "addEdgeMode") {
      console.log("addEdgeMode");
      state.network.addEdgeMode();
    }
  }

  // Watch for changes from Python
  model.on('change:nodes', update_nodes);
  model.on('change:edges', update_edges);
  model.on('change:manipulation_state', update_manipulation_state);
}
