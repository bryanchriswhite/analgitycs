import ApolloClient from 'apollo-boost';
import Vue from 'vue';
import VueApollo from 'vue-apollo';

import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';


const apolloClient = new ApolloClient({
    // You should use an absolute URL here
    uri: 'http://localhost:5000/graphql'
});

Vue.use(VueApollo);

const apolloProvider = new VueApollo({
    defaultClient: apolloClient,
});

Vue.config.productionTip = false;

new Vue({
    router,
    store,
    apolloProvider,
    vuetify,
    render: (h) => h(App)
}).$mount('#app');
