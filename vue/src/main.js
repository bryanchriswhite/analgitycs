import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import socketio from 'socket.io';
import VueSocketIO from 'vue-socket.io';

export const SocketInstance = socketio('http://localhost:5000');

Vue.use(VueSocketIO, SocketInstance, store);

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
