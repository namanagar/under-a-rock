<template>
  <div id="app">
    <Menu :options="this.options" @get-graphs="getGraphs" :filtered="boolSelected" @clear-nodes="clearNodes"></Menu>
    <div class="row" v-if="this.nodes.length != 0">
      <div class="col-xs-12 col-sm-12 col-md-6">
        <d3-network class="network" :net-nodes="scaledNodes" :net-links="links" :options="graphOptions" :selection="selection"
                    @node-click="selectNode"></d3-network>
      </div>
      <div class="col-xs-12 col-sm-12 col-md-6">
        <ArticleView ref="articleView" :articles="this.filteredArticles"></ArticleView>
      </div>
    </div>
  </div>
</template>

<script>
const axios = require("axios");
import D3Network from "vue-d3-network";
import ArticleView from "./components/ArticleView";
import Menu from "./components/Menu"
export default {
  name: "app",
  data() {
    return {
      options: [],
      nodes: [],
      edges: [],
      articles: [],
      selectedNodes: [],
      graphOptions: {
        canvas: false,
        force: 1100,
        strLinks: true,
        nodeLabels: true,
        //delete linkwidth when issue resolved with stroke width attribute below
        linkWidth: 3
      }
    };
  },
  mounted: function() {
     axios.get("https://underarock.tk/graphs/options").then(response => {
        this.options = response.data;
      })
  },
  computed: {
    links: function() {
      var links = [];
      this.edges.forEach(el => {
        let score = el.score
        links.push({
          id: el.id,
          sid: el.source,
          tid: el.target,
          name: el.id,
          //stroke width not currently working
          _svgAttrs: { "stroke-width" : el.score.toFixed(2) , 'stroke': "rgba(44, 62, 80, 0.4)"}
        });
      });
      return links;
    },
    scaledNodes: function() {
      var myNodes = [];
      this.nodes.forEach(el => {
        myNodes.push({ id: el.id, name: el.label.toLowerCase(), _size: this.getNodeSize(el.size) });
      });
      return myNodes;
    },
    selection: function() {
      var obj = {};
      obj.nodes = {};
      obj.links = {};
      this.selectedNodes.forEach(el => {
        obj.nodes[el.id] = el;
      });
      let edges = this.links;
      edges.forEach(edge => {
        if (this.selectedNodes.length > 0 & (this.selectedNodes.map(val => val.id).includes(edge.sid) && this.selectedNodes.map(val => val.id).includes(edge.tid))) {
          obj.links[edge.id] = edge;
        }
      });
      return obj;
    },
    keywords: function() {
      let arr = [];
      this.selectedNodes.forEach(el => {
        arr.push(el.id);
      });
      return arr;
    },
    filteredArticles: function() {
      let filtered = [];
      this.articles.forEach(el => {
        if (this.keywords.every(val => el.keywords.includes(val))) {
          filtered.push(el);
        }
      });
      return filtered;
    },
    boolSelected: function(){
      return (this.selectedNodes.length == 0) ? false : true
    }
  },
  methods: {
    getNodeSize(size){
      let newSize = size * 3
      if (newSize < 15) { return 15 }
      else if (newSize > 50) {  if (this.selected > 12) { return 40 } else { return 50 } }
      else return newSize
    },
    getGraphs(option) {
      this.selectedNodes = [];
      axios.get("https://underarock.tk/graphs/" + option).then(response => {
        this.nodes = response.data.nodes;
        this.edges = response.data.edges;
        this.articles = response.data.articles;
      });
    },
    selectNode(event, node) {
      this.selectedNodes.includes(node)
        ? this.selectedNodes.splice(this.selectedNodes.indexOf(node), 1)
        : this.selectedNodes.push(node);
    },
    clearNodes(){
      this.selectedNodes = []
    }
  },
  components: {
    D3Network,
    ArticleView,
    Menu
  }
};
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
}

h1,
h2,
h3 {
  font-family: "Lato", sans-serif;
}

h4,
h5,
h6 {
  font-family: "Work Sans", sans-serif;
}

p,
a {
  font-family: "Lato", sans-serif;
}

.padded {
  margin-top: 2em;
}

.network{
  max-height: 100%;
  max-width: 100%;
}
.node-label {
  font-family: "Lato", sans-serif;
  font-size: 0.85em;
  fill: rgba(44, 62, 80, 0.75);
}
@media screen and (max-width: 576px) { 
    .network{
      max-height: 75%;
    }
 }
.node {
  fill: #4cb191;
  stroke: #2c3e50;
  stroke-width: 2px;
}

.selected {
  stroke: #caa455 !important;
}

.link .selected {
  stroke: rgba(202, 164, 85, 0.6);
}

</style>
