import Vue from 'vue'
import Vuex from 'vuex'

import * as blame_manager from './blame_manager';
import * as blame_history from './blame_history';
import * as stackplot from './stackplot';
import * as theme from './theme';

Vue.use(Vuex)

export default new Vuex.Store({
    state: {},
    mutations: {},
    actions: {},
    modules: {
        theme: {namespaced: true, ...theme},
        stackplot: {namespaced: true, ...stackplot},
        blame_manager: {namespaced: true, ...blame_manager},
        blame_history: {namespaced: true, ...blame_history},
    }
})
