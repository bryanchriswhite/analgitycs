import Vue from 'vue'
import Vuex from 'vuex'

import {SET_COLOR, SET_LAYERS} from '@/store/actions'
import * as d3 from "d3";

Vue.use(Vuex)

const defaultColor = 'hsl(0, 10%, 20%)';
const initialColor = localStorage.getItem('color') || defaultColor;

let initialXMax = 0;
let initialYMax = 0;
let initialLayers = [];
const savedStackplot = localStorage.getItem('stackplot');
if (typeof (_layers) !== "undefined") {
    try {
        const stackplot = JSON.parse(savedStackplot);
        initialLayers = stackplot.stacked_layers;
        initialXMax = stackplot.xMax;
        initialYMax = stackplot.yMax;
    } catch (error) {
        console.error(error)
    }
}

export default new Vuex.Store({
    state: {
        color: initialColor,
        layers: initialLayers,
        xMax: initialXMax,
        yMax: initialYMax
    },
    mutations: {
        [SET_COLOR](state, color) {
            localStorage.setItem('color', color);
            state.color = color;
        },
        [SET_LAYERS](state, layers) {
            const input_layers = layers.map(layer => {
                return layer.map((n, i) => {
                    return {x: i * 50, y: n, y0: 0,}
                })
            })
            const stacked_layers = d3.layout.stack()(input_layers);
            const xMax = stacked_layers[0].length;
            const yMax = d3.max(stacked_layers[stacked_layers.length - 1].map(n => n.y + n.y0));
            const stackplot = {stacked_layers, xMax, yMax}
            localStorage.setItem('stackplot', JSON.stringify(stackplot));
            state.layers = stacked_layers;
            state.xMax = xMax;
            state.yMax = yMax;
        }
    },
    actions: {},
    modules: {}
})
