<template>
  <div>
    <Menu :clicked="true"></Menu>
    <div class="row no-gutters">
      <div class="col-xs-12 col-sm-12 col-lg-6">
         <div class="row no-gutters justify-content-center">
          <div class="col-sm-12">
            <vue-slider id="slider" :width="this.sliderWidth" v-bind="styling" :data="this.optionStrings" v-model="selected"></vue-slider>
          </div>
          <div class="col-sm-12" v-if="this.nodes.length != 0">
             <d3-network class="network" ref='net' :net-nodes="scaledNodes" :net-links="links" :options="graphOptions" :selection="selection"
                    @node-click="selectNode" @screen-shot="screenshotDone"></d3-network>
          </div>
          <div class="col-sm-12">
            <div v-if="!boolSelected">
              <h4 class="no-select">click nodes to filter articles</h4>
            </div>
            <div v-if="boolSelected">
              <h4 class="no-select" @click="clearNodes">click here to deselect all</h4>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xs-12 col-sm-12 col-lg-6" v-if="this.nodes.length != 0">
        <!-- <div class="row">
          <div class="col-xs-12 col-sm-12 col-lg-12" style="text-align: left">
            <span v-for="word in selectedNodes" :key="word" class="badge badge-pill badge-light no-select">{{word.id}}</span>
          </div>
        </div> -->
        <div class="row no-gutters semipadded">
          <ArticleView ref="articleView" :articles="this.filteredArticles"></ArticleView>
        </div>
      </div>
    </div>
    <div class="row no-gutters">
      <div class="col-sm-12 semipadded" v-if="clicked">
        <a style="color: #fff!important" href="https://goo.gl/forms/DXs7agQTxGFf1y593"><h2>give us feedback!</h2></a>
      </div>
    </div>
  </div>
</template>

<script>
const axios = require("axios");
import data from './graphs.js';
import D3Network from "vue-d3-network";
import ArticleView from "./ArticleView";
import Menu from "./Menu";
import vueSlider from "vue-slider-component";
export default {
  name: "UAR",
  data() {
    return {
      options: [],
      nodes: [],
      edges: [],
      articles: [],
      selectedNodes: [],
      graphOptions: {
        canvas: false,
        force: 1375,
        strLinks: true,
        nodeLabels: true,
        //delete linkwidth when issue resolved with stroke width attribute below
        linkWidth: 2
      },
      clicked: false,
      selected: this.$route.params.time,
      styling: {
        value: "slide",
        lazy: true,
        tooltip: "false",
        disabled: false,
        piecewise: true,
        piecewiseLabel: true,
        piecewiseStyle: {
          backgroundColor: "rgb(225, 225, 231)",
          visibility: "visible",
          width: "1em",
          height: "1em"
        },
        piecewiseActiveStyle: {
          backgroundColor: "rgb(32, 153, 115)"
        },
        labelActiveStyle: {
          color: "rgb(225, 225, 231)",
          fontFamily: "Work Sans",
          fontSize: "0.85em"
        },
        labelStyle: {
          color: "rgb(225, 225, 231)",
          fontFamily: "Work Sans",
          fontSize: "0.85em"
        },
        processStyle: {
          backgroundColor: "rgb(32, 153, 115)"
        }
      }
    };
  },
  mounted: function() {
    /* axios.get("https://underarock.tk/graphs/options").then(response => {
      this.options = response.data;
    });
    */
    this.options = [3,6,12,24,48,168];
    this.getGraphs(this.$route.params.time);
  },
  computed: {
    links: function() {
      var links = [];
      this.edges.forEach(el => {
        let score = el.score;
        links.push({
          id: el.id,
          sid: el.source,
          tid: el.target,
          name: el.id,
          //stroke width not currently working
          _svgAttrs: {
            "stroke-width": el.score.toFixed(2),
            stroke: "rgba(225, 225, 231, 0.6)"
          }
        });
      });
      return links;
    },
    scaledNodes: function() {
      var myNodes = [];
      this.nodes.forEach(el => {
        myNodes.push({
          id: el.id,
          name: el.label.toLowerCase(),
          _size: this.getNodeSize(el.size)
        });
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
        if (
          (this.selectedNodes.length > 0) &&
          (this.selectedNodes.map(val => val.id).includes(edge.sid) &&
            this.selectedNodes.map(val => val.id).includes(edge.tid))
        ) {
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
    boolSelected: function() {
      return this.selectedNodes.length == 0 ? false : true;
    },
    optionStrings(options) {
      var newArr = [];
      newArr.push("slide");
      this.options.forEach(option => {
        newArr.push(this.mapOptionStrToNum(option));
      });
      return newArr;
    },
    sliderWidth() {
      return "80%";
    }
  },
  methods: {
    mapOptionStrToNum(option) {
      return option == 168 ?
            option/168 + "w" :
            option/24 >= 1 ?
              option/24 + "d" :
              option + "h";
    },
    getNodeSize(size) {
      let newSize = size * 10;
      if (newSize < 15) {
        return 15;
      } else if (newSize > 50) {
        return 50;
      } else return newSize;
    },
    getGraphs(option) {
      this.selectedNodes = [];
      let result = data.filter(obj => { return obj.timecovered == 3600*option });
      this.nodes = result[0].json.nodes;
      this.edges = result[0].json.edges;
      this.articles = result[0].json.articles;
      /*axios.get("https://underarock.tk/graphs/" + option).then(response => {
        this.nodes = response.data.nodes;
        this.edges = response.data.edges;
        this.articles = response.data.articles;
      }); */

    },
    selectNode(event, node) {
      if (this.selectedNodes.includes(node)){
        this.selectedNodes.splice(this.selectedNodes.indexOf(node), 1);
      }
      else {
        this.selectedNodes.push(node);
        let selectedEdges = Object.keys(this.selection.links).map(key => this.selection.links[key]);
        var isLinked = false;
        selectedEdges.forEach(edge => {
          if (node == edge.source || node == edge.target){
            isLinked = true;
          }
        })
        if (!isLinked){
          this.selectedNodes = [];
          this.selectedNodes.push(node);
        }
      }
    },
    clearNodes() {
      this.selectedNodes = [];
    },
    getHoursFromString(str) {
      var digit = parseInt(str.match(/\d+/)[0]);
      if (str.indexOf("w") != -1){
        return digit * 24 * 7;
      }
      else if (str.indexOf("d") != -1) {
        return digit * 24;
      } else return digit;
    },
    takeScreenshot() {
      this.$refs.net.screenShot("Under-A-Rock");
    },
    screenshotDone() {
      console.log("screenshot saved");
      //TODO: export this png instead of saving to computer somehow
    }
  },
  watch: {
    selected: function(newSelected, oldSelected) {
      if (newSelected != oldSelected && newSelected != 'slide') {
        let newHours = this.getHoursFromString(newSelected);
        this.$router.push({ path: '/graphs/' + newHours, params: { newHours }});
      }
    },
    $route: function(to, from) {
      if (to != from && to.params.time != "slide") {
        this.getGraphs(to.params.time);
        this.selected = this.mapOptionStrToNum(to.params.time);
      }
    }
  },
  components: {
    D3Network,
    ArticleView,
    Menu,
    vueSlider
  }
}
</script>

<style>
.network {
  max-height: 100%;
  min-height: 60vh !important;
  max-width: 97.5% !important;
}
.node-label {
  font-family: "Lato", sans-serif;
  font-size: 0.85em;
  fill: rgba(225, 225, 231, 0.98);
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

.node {
  fill: rgb(32, 153, 115);
  stroke: rgba(225, 225, 231, 0.7);
  stroke-width: 1.5px;
}

.selected {
  stroke: #e4b95c !important;
  stroke-width: 2.5px;
}

.link .selected {
  stroke: rgba(202, 164, 85, 0.6);
  stroke-width: 4px;
}

#slider {
  margin-left: 5em;
}

.badge {
  font-family: "Work Sans";
  margin-left: 0.5em;
}

@media screen and (max-width: 576px) {
  #slider {
    margin-left: 2.25em;
    max-width: 95% !important;
  }
}
</style>
