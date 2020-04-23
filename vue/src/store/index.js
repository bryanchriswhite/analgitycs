import Vue from 'vue'
import Vuex from 'vuex'

import {SET_COLOR} from '@/store/actions'

Vue.use(Vuex)

const defaultColor = 'hsl(0, 10%, 20%)'
const initialColor = localStorage.getItem('color') || defaultColor

export default new Vuex.Store({
    state: {
        color: initialColor
    },
    mutations: {
        [SET_COLOR](state, color) {
            localStorage.setItem('color', color)
            state.color = color
        }
    },
    actions: {},
    modules: {}
})
