import * as ls from "./localstorage";

export const SET_REPOS = 'set_repos'
export const SET_RANGE_REF = 'set_range_ref'
export const SET_COMMIT_LIMIT = 'set_commit_limit'
export const SET_COMMIT_OFFSET = 'set_commit_offset'
export const BLAME_REPO = 'blame_repo'

const LOCAL_STORAGE_KEY = 'blame_manager'
const {save, load} = ls.factory(LOCAL_STORAGE_KEY)

const defaultCommitLimit = 10;
const defaultRangeRef = 'master';

let initialState = {
    range_ref: defaultRangeRef,
    commit_limit: defaultCommitLimit,
    commit_offset: 0,
    repos: [],
};

// TODO: remove!
initialState.repos.push({
    name: 'storj',
    url: '/home/bwhite/Projects/analgitycs/storj',
})

export const mutations = {
    [SET_REPOS](state, repos) {
        state.repos = repos;
        save(state)
    },
    [SET_RANGE_REF](state, range_ref) {
        console.log('SET_RANGE_REF called')
        state.range_ref = range_ref;
        save(state)
    },
    [SET_COMMIT_LIMIT](state, commit_limit) {
        state.commit_limit = commit_limit
        save(state)
    },
    [SET_COMMIT_OFFSET](state, commit_offset) {
        state.commit_offset = commit_offset
        save(state)
    }
};

export const actions = {
    // [BLAME_REPO](state, name) {
    //     // ...
    // },
}

export const state = load(initialState);
