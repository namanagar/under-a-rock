<template>
  <div id="menu">
    <div v-if="clicked === false" id="pre-click">
      <div class="row-fluid">
        <div class="col-sm-12 col-md-12">
          <img id="logo" src="../assets/logo.png">
          <h3>under a rock<span style="font-size: 2em; color: #4CB191">.</span><small class="text-muted" style="font-size: 0.35em">(alpha)</small></h3>
        </div>
      </div>
      <div class="row-fluid padded">
        <div class="col-sm-12 col-md-12">
          <h4>how long have you been under a rock?</h4>
        </div>
      </div>
      <div class="row-fluid semipadded">
        <div class="col-sm-12 col-md-12">
          <div class="row justify-content-center" v-if="this.optionStrings.length > 0">
            <vue-slider v-bind="styling" :data="this.optionStrings" v-model="selected"></vue-slider>
        </div>
      </div>
    </div>
  </div>
  <div v-if="clicked === true" id="post-click">
    <nav class="navbar">
      <a class="navbar-brand">
        <img id="logoClicked" src="../assets/logo.png" alt="Logo">
      </a>
      <div v-if="!filtered">
        <h4>click nodes to filter articles</h4>
      </div>
      <div v-if="filtered">
        <h4 @click="clear">click here to deselect all</h4>
      </div>
      <div>
        <vue-slider id="slider" v-bind="styling" :data="this.optionStrings" v-model="selected"></vue-slider>
      </div>
    </nav>
    </div>
  </div>
</template>
<script>
import vueSlider from 'vue-slider-component';
export default {
  name: "Menu",
  props: ["options", "filtered"],
  data() {
    return {
      selected: 'slide to pick',
      clicked: false,
      styling: {
        value: 'slide to pick',
        lazy: true,
        width: "70%",
        tooltip: "false",
        disabled: false,
        piecewise: true,
        piecewiseLabel: true,
        piecewiseStyle: {
          "backgroundColor": "rgb(225, 225, 231)",
          "visibility": "visible",
          "width": "1em",
          "height": "1em"
        },
        piecewiseActiveStyle: {
          "backgroundColor": "rgb(32, 153, 115)"
        },
        labelActiveStyle: {
          "color": "rgb(225, 225, 231)",
          "fontFamily": "Work Sans",
          "fontSize": "0.85em"
        },
        labelStyle: {
          "color": "rgb(225, 225, 231)",
          "fontFamily": "Work Sans",
          "fontSize": "0.85em"
        },
        processStyle: {
          "backgroundColor": "rgb(32, 153, 115)"
        }
      }
    };
  },
  methods: {
    getGraphs(option){
      this.clicked = true
      this.$emit("get-graphs", option)
    },
    clear(){
      this.$emit("clear-nodes")
    },
    getHoursFromString(str){
      // "2 days" -> 48 or "8 hours" -> 8
      var digit = parseInt(str.match(/\d+/)[0])
      if (str.indexOf("day") != -1){
        return digit * 24;
      }
      else return digit;
    }
  },
  computed: {
     optionStrings(options) {
      var newArr = []
      newArr.push("slide to pick")
      this.options.forEach(option => {
        newArr.push(option < 24
          ? option + " hours"
          : option / 24 > 1 ? option / 24 + " days" : option / 24 + " day")
      });
      return newArr;
    }
  },
  watch: {
    selected: function(newSelected, oldSelected){
      if (newSelected != oldSelected){
        this.getGraphs(this.getHoursFromString(newSelected))
      }
    }
  },
  components: {
    vueSlider
  }
};
</script>
<style scoped>

  #logo {
    max-width: 50vmin;
  }

  #logoClicked {
    max-width: 9vh;
    max-height: 9vh;
  }

  [type="radio"] {
    display: none;
  }

  #post-click{
    max-height: 15vh;
    text-align: left;
  }

  #pre-click{
    margin-top: 40px;
  }

  @media screen and (max-width: 576px) {
    #logoClicked{
      display: none !important;
    }
    #options input{
      font-size: .5em;
    }
    #post-click{
      max-height: 10vh;
    }
  }

  #slider{
    min-width: 50%;
  }
</style>
