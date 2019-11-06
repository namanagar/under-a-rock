<template>
  <div>
    <Menu :clicked="false"></Menu>
    <div class="row no-gutters">
      <div class="col-sm-12 col-md-12">
        <div class="row no-gutters justify-content-center" id="sliderContainer" v-if="this.optionStrings.length > 0">
          <vue-slider :width="this.sliderWidth" v-bind="styling" :data="this.optionStrings" v-model="selected"></vue-slider>
        </div>
      </div>
    </div>
    <div class="row no-gutters extrapadded justify-content-md-center">
      <div class="col-sm-8">
        <div>
          <div class="card-body">
            <h2 class="card-title">what do i do?</h2>
             <p style="font-family: Work Sans">
              just select the time period (in hours or days) you want to catch up on using the slider 
              and a graph will appear. the bubbles' size depends on how often the topic shows up in the news.
              clicking bubbles will filter the list of articles to give you the news you care about.
            </p>
            <h2 style="margin-top: 1em;" class="card-title">about us</h2>
            <p style="font-family: Work Sans">
              <span style="font-family: Lato">under a rock<span style="font-size: 2em; color: #4CB191">.</span></span> is a unique news aggregator, 
              displaying the world’s top trending news in the form of a web. 
              the network allows you to see the relationships between articles from around the world, 
              giving them meaning in a larger context.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const axios = require("axios");
import Menu from "./Menu";
import vueSlider from "vue-slider-component";
export default {
  name: "Home",
  data() {
    return {
      options: [],
      selected: "slide",
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
    axios.get("https://underarock.tk/graphs/options").then(response => {
      this.options = response.data;
    });
  },
  computed: {
    optionStrings(options) {
      var newArr = [];
      newArr.push("slide");
      this.options.forEach(option => {
        newArr.push(
          option == 168 ?
            option/168 + "w" :
            option/24 >= 1 ?
              option/24 + "d" :
              option + "h"
        );
      });
      return newArr;
    },
    sliderWidth() {
      if (window.innerWidth < 576) {
        return "95%";
      } else return "60%";
    }
  },
  methods: {
    getGraphs(option) {
      let allOptions = this.options;
      console.log(allOptions)
      this.$router.push({ path: '/graphs/' + option, params: { 'time': option }});
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
  },
  watch: {
    selected: function(newSelected, oldSelected) {
      if (newSelected != oldSelected) {
        this.clicked = true;
        this.getGraphs(this.getHoursFromString(newSelected));
      }
    }
  },
  components: {
    Menu,
    vueSlider
  }
};
</script>

<style>
@media screen and (max-width: 576px) {
  #slider {
    margin-left: 2.25em;
    max-width: 95% !important;
  }
}
</style>
