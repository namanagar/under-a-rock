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
    <div class="row-fluid">
      <div class="col-sm-12 col-md-12">
        <div class="row justify-content-center">
          <div v-for="option in this.options" :key="option" id="options">
            <label :class="[(option == selected) ? 'btn btn-light' : 'btn btn-outline-light']">
              <input type="radio" name="options" autocomplete="off" :value="option" v-model="selected" @click="getGraphs(option)">{{ getOptionString(option) }}
            </label>
          </div>
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
          <div v-for="option in this.options" :key="option" class="btn-group inline" id="options">
                    <label :class="[(option == selected) ? 'btn btn-sm btn-light' : 'btn btn-sm btn-outline-light']">
                        <input type="radio" name="options" autocomplete="off" :value="option" v-model="selected" @click="getGraphs(option)">{{ getOptionString(option) }}
                    </label>
                </div>
        </nav>
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
</style>
