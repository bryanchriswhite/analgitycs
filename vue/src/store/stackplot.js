import * as d3 from "d3";

import * as ls from "./localstorage";

export const SET_LAYERS = 'set_layers';
export const SET_AUTHORS = 'set_authors';
export const SET_ACTIVE_LAYER = 'set_active_layer';

const LOCAL_STORAGE_KEY = 'stackplot';
const {load} = ls.factory(LOCAL_STORAGE_KEY);

let initialState = {
    xMax: 0,
    yMax: 0,
    layers: [],
    active_layer: null,
};

export const mutations = {
    [SET_LAYERS](state, layers) {
        const input_layers = layers.map(layer => {
            return layer.map((n, i) => {
                return {x: i, y: n, y0: 0,}
            })
        })
        state.layers = d3.layout.stack()(input_layers);

        if (!layers || layers.length < 1) return;

        state.xMax = state.layers[0].length;
        state.yMax = d3.max(state.layers[state.layers.length - 1].map(n => n.y + n.y0));
        // save(state);
    },
    [SET_AUTHORS](state, authors) {
        state.authors = authors
    },
    [SET_ACTIVE_LAYER](state, layer_index) {
        state.active_layer = layer_index;
    },
};

export const state = load(initialState);
