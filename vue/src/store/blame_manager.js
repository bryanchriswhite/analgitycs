import * as fetch from 'd3-fetch';

import * as ls from "./localstorage";
import {SET_LAYERS, SET_AUTHORS} from './stackplot'
// import * as _ from "lodash";

// Mutations
export const ADD_REPO = 'add_repo'
export const DEL_REPO = 'delete_repo'
export const SET_RANGE_REF = 'set_range_ref'
export const SET_COMMIT_LIMIT = 'set_commit_limit'
export const SET_COMMIT_OFFSET = 'set_commit_offset'
export const SET_BLAME = 'set_blame'
export const SET_EXT_WLIST = 'set_ext_whitelist'
export const SET_MAX_WORKTREES = 'set_max_worktrees'
export const SET_MAX_WORKERS = 'set_max_workers'

// Actions
export const BLAME_REPO = 'blame_repo'
export const DEL_BLAME = 'delete_blame'
export const CHECK_BLAME = 'check_blame'

const LOCAL_STORAGE_KEY = 'blame_manager'
const {save, load} = ls.factory(LOCAL_STORAGE_KEY)

const defaultCommitLimit = 500;
const defaultMaxWorktrees = 125;
const defaultMaxWorkers = 10;
const defaultRangeRef = 'master';

const baseUrl = 'http://localhost:5000/repo/';
const fetchBase = {
    mode: 'cors',
    headers: [['content-type', 'application/json']]
};

let initialState = {
    range_ref: defaultRangeRef,
    commit_limit: defaultCommitLimit,
    max_worktrees: defaultMaxWorktrees,
    max_workers: defaultMaxWorkers,
    commit_offset: 0,
    ext_whitelist: '.go,.proto,.c,.h,.sh,.md,.xml,.wixproj,.wsx,.cs',
    repos: {},
    blames: {},
};

export const mutations = {
    [ADD_REPO](state, {name, path, url}) {
        state.repos[name] = {name, path, url};
        save(state)
    },
    [DEL_REPO](state, name) {
        delete state.repos[name]
        save(state)
    },
    [SET_RANGE_REF](state, {target: {value}}) {
        // console.log('SET_RANGE_REF called')
        state.range_ref = value;
        save(state)
    },
    [SET_COMMIT_LIMIT](state, {target: {value}}) {
        state.commit_limit = value
        save(state)
    },
    [SET_COMMIT_OFFSET](state, {target: {value}}) {
        state.commit_offset = value
        save(state)
    },
    [SET_EXT_WLIST](state, {target: {value}}) {
        state.ext_whitelist = value
        save(state)
    },
    [SET_BLAME](state, {name, ...payload}) {
        // if (!state.blames) {
        //     state.blames = {}
        // }
        //
        // if (!state.balmes[name]) {
        //     state.blames[name] = []
        // }
        //
        // state.blames[name].push(payload)
        let blame = state.blames[name]
        if (!blame) {
            blame = state.blames[name] = {recent: []}
        }
        blame.recent.push(blame.last);
        blame.last = payload;
        save(state)
    },
    [DEL_BLAME](state, name) {
        // delete state.blames[name]
        if (state.blames[name]) {
            delete state.blames[name].current
        }
        save(state)
    },
    [SET_MAX_WORKTREES](state, {target: {value}}) {
        state.max_worktrees = value
    },
    [SET_MAX_WORKERS](state, {target: {value}}) {
        state.max_workers = value
    },
};


const logError = (error) => {
    // TODO: error handling!
    console.error(error)
}

export const actions = {
    [BLAME_REPO]({commit, state: {range_ref, commit_limit, max_worktrees, ext_whitelist}}, name) {
        ext_whitelist = ext_whitelist.split(',')
        console.log(ext_whitelist)
        const params = {range_ref, commit_limit, ext_whitelist};

        const putSuccess = (result) => {
            console.log('blame success!')
            console.log(result)

            if (!result.status.done) return

            // that.$store.commit('stackplot/' + SET_LAYERS, result.layers)
            commit('stackplot/' + SET_AUTHORS, result.authors, {root: true})
            commit('stackplot/' + SET_LAYERS, result.layers, {root: true})
            commit(SET_BLAME, {name, params, result})
        }

        const postSuccess = () => {
            fetch.json(baseUrl + name,
                {
                    // method: 'GET',
                    method: 'PUT',
                    body: JSON.stringify(params),
                    ...fetchBase
                })
                // TODO: something else
                .then(putSuccess, logError)
        }

        const {path, url} = state.repos[name]
        const repoParams = {path, url, max_worktrees}

        fetch.json(baseUrl + name, {
            method: 'POST',
            body: JSON.stringify(repoParams),
            ...fetchBase
        }).then(postSuccess, logError)
    },
    [DEL_BLAME]({commit}, name) {
        fetch.json(baseUrl + name,
            {
                method: 'DELETE',
                ...fetchBase
            }).then(() => commit(DEL_BLAME, name), logError)
        // }).then(() => commit(DEL_REPO, name), logError)
    },
    [CHECK_BLAME]({commit, state: {range_ref, commit_limit, max_worktrees, ext_whitelist}}, name) {
        console.log('action called')
        ext_whitelist = ext_whitelist.split(',')
        const params = {range_ref, commit_limit, max_worktrees, ext_whitelist};

        const putSuccess = (result) => {
            console.log('blame success!')
            console.log(result)

            if (!result.status.done) return

            // that.$store.commit('stackplot/' + SET_LAYERS, result.layers)
            commit('stackplot/' + SET_AUTHORS, result.authors, {root: true})
            commit('stackplot/' + SET_LAYERS, result.layers, {root: true})
            commit(SET_BLAME, {name, params, result})
        }

        fetch.json(baseUrl + name,
            {
                method: 'GET',
                ...fetchBase
            })
            // TODO: something else
            .then(putSuccess, logError)
    },
}

export const state = load(initialState);
