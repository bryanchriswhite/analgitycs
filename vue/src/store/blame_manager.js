import * as fetch from 'd3-fetch';

import * as ls from "./localstorage";
import {SET_LAYERS} from './stackplot'
import * as _ from "lodash";

// Mutations
export const ADD_REPO = 'add_repo'
export const DEL_REPO = 'delete_repo'
export const SET_RANGE_REF = 'set_range_ref'
export const SET_COMMIT_LIMIT = 'set_commit_limit'
export const SET_COMMIT_OFFSET = 'set_commit_offset'
export const SET_BLAME = 'set_blame'
export const SET_EXT_WLIST = 'set_ext_whitelist'

// Actions
export const BLAME_REPO = 'blame_repo'

const LOCAL_STORAGE_KEY = 'blame_manager'
const {save, load} = ls.factory(LOCAL_STORAGE_KEY)

const defaultCommitLimit = 10;
const defaultRangeRef = 'master';

let initialState = {
    range_ref: defaultRangeRef,
    commit_limit: defaultCommitLimit,
    commit_offset: 0,
    ext_whitelist: ['.go', '.proto', '.c', '.h', '.sh', '.md', '.xml', '.wixproj', '.wsx', '.cs'],
    repos: {},
};

export const mutations = {
    [ADD_REPO](state, {name, path, url}) {
        state.repos[name] = {name, path, url};
        save(state)
    },
    [DEL_REPO](state, name) {
        const i = _.findIndex(state.repos, e => e.name === name)
        if (i < 0) {
            console.error(`repo ${name} not added`)
            return
        }

        state.repos.splice(i, 1)
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
    },
    [SET_BLAME](state, {name, ...payload}) {
        if (!state.blames) {
            state.blames = {}
        }

        if (!state.balmes[name]) {
            state.blames[name] = []
        }

        state.blames[name].push(payload)
    }
};

const baseUrl = 'http://localhost:5000/repo/';
const fetchBase = {
    mode: 'cors',
    headers: [['content-type', 'application/json']]
};
// fetch.json('http://localhost:5000/repo/storj', {mode: 'cors'}).then()

export const actions = {
    [BLAME_REPO]({commit, state: {range_ref, commit_limit, ext_whitelist}}, name) {
        const params = {
            range_ref,
            commit_limit,
            ext_whitelist
        };

        console.log(state.repos[name])
        const {path, url} = state.repos[name]
        const repoParams = {name, path, url}
        // const repoParams = {}
        fetch.json(baseUrl + name, {
            method: 'POST',
            body: JSON.stringify(repoParams),
            ...fetchBase
        }).then(function () {
            fetch.json(baseUrl + name,
                {
                    method: 'PUT',
                    body: JSON.stringify(params),
                    ...fetchBase
                })
                // TODO: something else
                .then(function (result) {
                    console.log('blame success!')
                    console.log(result)
                    // that.$store.commit('stackplot/' + SET_LAYERS, result.layers)
                    commit('stackplot/' + SET_LAYERS, result.layers, {root: true})
                    commit(SET_BLAME, {name, params, result})
                }, function (error) {
                    // TODO: error handling!
                    console.error('blame error!')
                    console.error(error)
                })
        }, function (error) {
            console.error('repo error!')
            console.error(error)
        })
    },
}

export const state = load(initialState);
