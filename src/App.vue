<template>
  <div id="app" class="container">
    <div class="row-fluid">
      <div class="col-sm-12 col-md-12">
        <img id="logo" src="./assets/logo.png">
        <h2>under a rock<span style="font-size: 2em; color: #4CB191">.</span></h2>
      </div>
    </div>
    <div class="row-fluid padded">
      <div class="col-sm-12 col-md-12">
        <h4>how long have you been under a rock?</h4>
      </div>
    </div>
    <div class="row-fluid">
      <div class="col-sm-12 col-md-12">
        <div class="row justify-content-center">
          <div v-for="option in this.options" :key="option">
            <label :class="[(option == selected) ? 'btn btn-secondary' : 'btn btn-outline-secondary']">
              <input type="radio" name="options" autocomplete="off" :value="option" v-model="selected" @click="getGraphs(option)">{{ getOptionString(option) }}
            </label>
          </div>
        </div>
      </div>
    </div>
    <div class="row-fluid" v-if="this.selected != ''">
      <div class="col-sm-12 col-md-12">
        <d3-network :net-nodes="scaledNodes" :net-links="links" :options="graphOptions" :selection="selection"
                    @node-click="selectNode"></d3-network>
      </div>
    </div>
    <div class="row-fluid padded" v-if="this.flattenedArticles.length > 0">
      <div class="col-sm-12 col-md-12">
        <h4>filtered articles</h4>
      </div>
    </div>
    <div class="row-fluid padded" v-if="this.filteredArticles.length > 0">
      <div class="col-sm-12 col-md-12">
        <ArticleView :articles="this.filteredArticles"></ArticleView>
      </div>
    </div>
  </div>
</template>

<script>
const axios = require("axios");
import D3Network from "vue-d3-network";
import ArticleView from "./components/ArticleView";
export default {
  name: "app",
  data() {
    return {
      options: [3, 6, 12, 24, 48],
      selected: "",
      nodes: [],
      edges: [],
      articles: [],
      selectedNodes: [],
      graphOptions: {
        canvas: false,
        force: 3000,
        linkWidth: 3,
        strLinks: true,
        nodeLabels: true
      }
    };
  },
  computed: {
    links: function() {
      var links = [];
      this.edges.forEach(el => {
        links.push({
          id: el.id,
          sid: el.source,
          tid: el.target,
          name: el.id,
          _color: "rgba(44, 62, 80, 0.4)"
        });
      });
      return links;
    },
    scaledNodes: function() {
      var myNodes = [];
      this.nodes.forEach(el => {
        myNodes.push({ id: el.id, name: el.label, _size: el.size * 4 });
      });
      return myNodes;
    },
    selection: function() {
      var obj = {};
      obj.nodes = {};
      obj.links = {};
      this.selectedNodes.forEach(el => {
        obj.nodes[el.id] = el;
        let node = el.id;
        let edges = this.links;
        edges.forEach(edge => {
          if (edge.tid === node || edge.sid === node) {
            obj.links[edge.id] = edge;
          }
        });
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
    flattenedArticles: function() {
      let flat = [];
      this.articles.forEach(el => {
        let article = {};
        let key = Object.keys(el)[0];
        article.link = key;
        article.name = el[key].name;
        article.title = el[key].title;
        article.keywords = el[key].keywords;
        flat.push(article);
      });
      return flat;
    },
    filteredArticles: function() {
      let filtered = [];
      this.flattenedArticles.forEach(el => {
        if (this.keywords.every(val => el.keywords.includes(val))) {
          filtered.push(el);
        }
      });
      return filtered;
    }
  },
  methods: {
    getOptionString(option) {
      return option < 24
        ? option + " hours"
        : option / 24 > 1 ? option / 24 + " days" : option / 24 + " day";
    },
    getGraphs(option) {
      this.selectedNodes = [];
      axios.get("http://167.99.154.215/graphs/" + option).then(response => {
        this.nodes = response.data.nodes;
        this.edges = response.data.edges;
        this.articles = response.data.articles;
      });
    },
    selectNode(event, node) {
      this.selectedNodes.includes(node)
        ? this.selectedNodes.splice(this.selectedNodes.indexOf(node), 1)
        : this.selectedNodes.push(node);
    }
  },
  components: {
    D3Network,
    ArticleView
  }
};
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  margin-bottom: 60px;
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

#logo {
  max-width: 50vmin;
}

.padded {
  margin-top: 2em;
}

[type="radio"] {
  display: none;
}

.node-label {
  font-family: "Lato", sans-serif;
  font-size: 0.85em;
  fill: rgba(44, 62, 80, 0.75);
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
