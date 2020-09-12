import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import vuescrollmagic from './plugins/vue-scrollmagic.js'
import axios from 'axios'

Vue.config.productionTip = false
Vue.prototype.$axios = axios 

new Vue({
  router,
  vuetify,
  vuescrollmagic,
  render: h => h(App)
}).$mount('#app')
