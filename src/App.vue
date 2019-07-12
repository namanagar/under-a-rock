<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #fff;
  margin-top: 5px;
  margin-bottom: 5vh;
  max-width: 100vw !important;
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
.semipadded {
  margin-top: 1.5em;
}
.extrapadded {
  margin-top: 5em;
}
.no-select {
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

</style>