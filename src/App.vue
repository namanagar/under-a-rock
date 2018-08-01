<template>
  <div id="app">
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
  </div>
</template>

<script>
const axios = require('axios');
export default {
  name: 'app',
  data () {
    return {
      options: [3,6,12,24,48],
      selected: '',
      info: ''
    }
  },
  methods: {
    getOptionString(option){
      return (option < 24) ? option + " hours" : (option/24 > 1) ? option/24 + " days" : option/24 + " day";
    },
    getGraphs(option){
      axios
      .get('http://167.99.154.215/graphs/' + option)
      .then(response => (this.info = response))
    }
  }
}
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1, h2, h3 {
  font-family: 'Lato', sans-serif;
}

h4, h5, h6{
  font-family: 'Work Sans', sans-serif;
}

p, a, span {
  font-family: 'Merriweather', serif;
}

#logo{
  max-width: 50vmin;
}
.padded{
  margin-top: 2em;
}
[type='radio'] {
display: none; 
}
</style>
