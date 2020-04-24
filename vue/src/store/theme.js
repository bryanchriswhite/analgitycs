import * as ls from "./localstorage";

export const SET_COLOR = 'set_color';

const LOCAL_STORAGE_KEY = 'theme';
const {save, load} = ls.factory(LOCAL_STORAGE_KEY)

const initialState = {
    color: 'hsl(0, 10%, 20%)'
};

export const mutations = {
    [SET_COLOR](state, color) {
        state.color = color;
        save(state);
    }
};

export const state = load(initialState);
