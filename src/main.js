import Vue from 'vue';
import App from './App.vue';
import UAR from './components/UAR.vue';
import Home from './components/Home.vue';
import VueRouter from 'vue-router';
Vue.use(VueRouter);

const routes = [
  { path: '/', component: Home},
  { path: '/graphs/:time', component: UAR}
]

const router = new VueRouter({
  routes
})

const app = new Vue({
  router,
  el: '#app',
  render: h => h(App)
})
