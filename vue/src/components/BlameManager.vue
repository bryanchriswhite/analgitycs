<template>
    <section>
        <h2>Blame Manager</h2>
        <section>
            <input name="range_ref"
                   type="text"
                   placeholder="range_ref"
                   @change="setRangeRef"
                   :value="range_ref"/>
            <input name="commit_limit"
                   type="text"
                   placeholder="commit limit"
                   @change="setCommitLimit"
                   :value="commit_limit"/>
            <input name="commit_offset"
                   type="text"
                   placeholder="commit offset"
                   @change="setCommitOffset"
                   :value="commit_offset"/>
        </section>
        <section v-for="repo in repos" :key=repo.name>
            <button @click="blame(repo.name)">Blame</button>
            <span>{{repo.name}}</span>
            <button @click="delete_repo(repo.name)">x</button>
        </section>
        <section>
            <input name="new_repo_name"
                   type="text"
                   placeholder="name"
                   v-model="new_repo_name"/>
            <input name="new_repo_url"
                   type="text"
                   placeholder="url"
                   v-model="new_repo_url"/>
            <button @click="add_repo">+</button>
        </section>
    </section>
</template>

<style scoped lang="stylus">
    input, button
        padding 5px
        margin 5px
</style>

<script>
    import {mapState} from 'vuex';
    import * as _ from 'lodash';
    import * as fetch from 'd3-fetch';

    import {SET_LAYERS} from '@/store/stackplot'
    import {
        SET_REPOS,
        SET_RANGE_REF,
        SET_COMMIT_LIMIT,
        SET_COMMIT_OFFSET
    } from '@/store/blame_manager'

    const baseUrl = 'http://localhost:5000/repo/';
    const fetchBase = {
        mode: 'cors',
        headers: [['content-type', 'application/json']]
    };
    // fetch.json('http://localhost:5000/repo/storj', {mode: 'cors'}).then()

    const ext_whitelist = [".go", ".proto", ".c", ".h", ".sh", ".md", ".xml", ".wixproj", ".wsx", ".cs"]

    export default {
        name: 'BlameManager',
        // TODO: move to store?
        data: () => ({
            new_repo_name: '',
            new_repo_url: '',
            // repos: []
        }),
        // TODO: use constant!
        computed: mapState('blame_manager', [
            'repos',
            'range_ref',
            'commit_limit',
            'commit_offset'
        ]),
        methods: {
            setRangeRef(evt) {
                this.$store.commit('blame_manager/' + SET_RANGE_REF, evt.target.value)
            },
            setCommitLimit(evt) {
                this.$store.commit('blame_manager/' + SET_COMMIT_LIMIT, evt.target.value)
            },
            setCommitOffset(evt) {
                this.$store.commit('blame_manager/' + SET_COMMIT_OFFSET, evt.target.value)
            },
            add_repo() {
                const {repos} = this.$store.state.blame_manager
                const {new_repo_name: name, new_repo_url: url} = this
                this.$store.commit('blame_manager/' + SET_REPOS, [...repos, {name, url}])
                this.new_repo_name = ''
                this.new_repo_url = ''
            },
            delete_repo(name) {
                const {repos} = this.$store.state.blame_manager
                const i = _.findIndex(repos, e => e.name === name)
                if (i < 0) {
                    console.error(`repo ${name} not added`)
                    return
                }

                repos.splice(i, 1)
                this.$store.commit('blame_manager/' + SET_REPOS, repos)
            },
            // TODO: make an action instead!
            blame(name) {
                const that = this
                fetch.json(baseUrl + name,
                    {
                        method: 'PUT',
                        body: JSON.stringify({
                            range_ref: that.range_ref,
                            commit_limit: that.commit_limit,
                            // commit_offset: that.commit_offset,
                            ext_whitelist,
                        }),
                        ...fetchBase
                    })
                    // TODO: something else
                    .then(function (res) {
                        console.log('blame success!')
                        console.log(res)
                        that.$store.commit('stackplot/' + SET_LAYERS, res.layers)
                    }, function (error) {
                        // TODO: better error handling!
                        console.error('blame error!')
                        console.error(error)
                    })
            },
            // ...mapActions({})
        }
    }
</script>