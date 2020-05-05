export const SELECT_REPO = 'select_repo';

export const state = {
    selectedRepo: '',
};

export const mutations = {
    [SELECT_REPO](state, {target: {value}}) {
        state.selectedRepo = value;
    },
};