<template>
  <div id="menu">
    <div v-if="this.clicked === false" id="pre-click">
      <div class="row-fluid">
        <div class="col-sm-12 col-md-12">
          <img id="logo" src="../assets/logo.png">
          <h3>under a rock<span style="font-size: 2em; color: #4CB191">.</span><small style="font-size: 0.35em">(beta)</small></h3>
        </div>
      </div>
       <div class="row-fluid">
        <div class="col-sm-12 col-md-12">
          <small class="no-select" @click="showModal = true">about/how to</small>
        </div>
      </div>
      <div class="row-fluid padded">
        <div class="col-sm-12 col-md-12">
          <h4>how long have you been under a rock?</h4>
        </div>
      </div>
  </div>
  <div v-if="this.clicked === true" id="post-click">
    <nav class="navbar">
      <div class="navbar-brand">
        <img id="logoClicked" src="../assets/logo.png" alt="Logo">
      </div>
      <div>
        <h5 class="no-select" @click="showModal = true">about under a rock</h5>
      </div>
    </nav>
  </div>
  <about-modal @close="showModal = false" v-if="showModal"></about-modal>
  </div>
</template>
<script>
import AboutModal from './AboutModal'
export default {
  name: "Menu",
  props: ["clicked"],
  data() {
    return {
      showModal: false
    };
  },
  methods: {
  },
  components: {
    AboutModal
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
    max-height: 10vh;
    text-align: left;
  }

  #pre-click{
    margin-top: 40px;
  }
  small{
    font-family: "Work Sans";
  }
  @media screen and (max-width: 576px) {
    #options input{
      font-size: .5em;
    }
    #post-click{
      max-height: 10vh;
    }
  }
</style>
