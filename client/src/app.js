import Vue from 'vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'font-awesome/scss/font-awesome.scss';

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

import App from "./App.vue"

new Vue({
  el: '#app',
  template: '<App/>',
  components: { App},
  render: h => h(App)
})