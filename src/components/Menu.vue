<template>
  <div id="menu">
    <div v-if="clicked === false" id="pre-click">
    <div class="row-fluid">
      <div class="col-sm-12 col-md-12">
        <img id="logo" src="../assets/logo.png">
        <h3>under a rock<span style="font-size: 2em; color: #4CB191">.</span></h3>
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
          <div v-for="option in this.options" :key="option" id="options">
            <label :class="[(option == selected) ? 'btn btn-secondary' : 'btn btn-outline-secondary']">
              <input type="radio" name="options" autocomplete="off" :value="option" v-model="selected" @click="getGraphs(option)">{{ getOptionString(option) }}
            </label>
          </div>
        </div>
      </div>
    </div>
    </div>
    <div v-if="clicked === true" id="post-click">
        <div class="row-fluid" id="postrow">
            <div class="span4" id="titleClicked">
                <img id="logoClicked" src="../assets/logo.png">
            </div>
             <div class="span4 ml-auto" v-if="!filtered">
                <h4>click on nodes to filter articles</h4>
            </div>
            <div class="span4 ml-auto" v-if="filtered">
                <h4 @click="clear">click here to deselect all</h4>
            </div>
            <div class="span4 ml-auto">
                <div v-for="option in this.options" :key="option" class="btn-group inline" id="options">
                    <label :class="[(option == selected) ? 'btn btn-sm btn-secondary' : 'btn btn-sm btn-outline-secondary']">
                        <input type="radio" name="options" autocomplete="off" :value="option" v-model="selected" @click="getGraphs(option)">{{ getOptionString(option) }}
                    </label>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "Menu",
  props: ["options", "filtered"],
  data() {
    return {
        selected: '',
        clicked: false
    };
  },
  methods: {
    getOptionString(option) {
      return option < 24
        ? option + " hours"
        : option / 24 > 1 ? option / 24 + " days" : option / 24 + " day";
    },
    getGraphs(option){
        this.clicked = true
        this.$emit("get-graphs", option)
    },
    clear(){
      this.$emit("clear-nodes")
    }
  }
};
</script>
<style scoped>

#logo {
  max-width: 50vmin;
}

#logoClicked {
    max-width: 15vmin;
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

#postrow{
    display: table;
    vertical-align:middle;
}

.span4{
    display: table-cell;
    float: none;
    width: 15%;
}

@media screen and (max-width: 576px) { 
    #titleClicked{
        display: none !important;
    }
    #options input{
      font-size: .5em;
    }
    #post-click{
      max-height: 10vh;
    }
 }
</style>
