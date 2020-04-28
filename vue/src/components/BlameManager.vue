<template>
    <section class="blame">
        <h2>Blame Manager</h2>
        <section class="blame_params">
            <input name="range_ref"
                   type="text"
                   placeholder="range_ref"
                   @change="set_range_ref"
                   :value="range_ref"/>
            <input name="commit_limit"
                   type="text"
                   placeholder="commit limit"
                   @change="setCommitLimit"
                   :value="commit_limit"/>
            <input name="ext_whitelist"
                   type="text"
                   placeholder="file ext whitelist"
                   @change="set_ext_whitelist"
                   :value="ext_whitelist"/>
            <!--            <input name="commit_offset"-->
            <!--                   type="text"-->
            <!--                   placeholder="commit offset"-->
            <!--                   @change="setCommitOffset"-->
            <!--                   :value="commit_offset"/>-->
        </section>
        <section class="repo_params">
            <input name="new_repo_name"
                   type="text"
                   placeholder="name"
                   v-model="new_repo_name"/>
            <!--            <input name="new_repo_url"-->
            <!--                   type="text"-->
            <!--                   placeholder="url"-->
            <!--                   v-model="new_repo_url"/>-->
            <input name="new_repo_path"
                   type="text"
                   placeholder="path"
                   v-model="new_repo_path"/>
            <button @click="add_repo">+</button>
        </section>
        <section class="repos">
            <section v-for="repo in repos" :key=repo.name>
                <button @click="blame_repo(repo.name)">Blame</button>
                <span>{{repo.name}}</span>
                <button @click="delete_repo(repo.name)">x</button>
            </section>
        </section>
    </section>
</template>

<style scoped lang="stylus">
    input, button
        padding 5px
        margin 5px
</style>

<script>
    import {mapState, mapMutations, mapActions} from 'vuex';

    import {
        ADD_REPO,
        DEL_REPO,
        SET_RANGE_REF,
        SET_COMMIT_LIMIT,
        SET_COMMIT_OFFSET,
        SET_EXT_WLIST,
        BLAME_REPO
    } from '@/store/blame_manager'

    export default {
        name: 'BlameManager',
        // TODO: move to store?
        data: () => ({
            new_repo_name: '',
            new_repo_url: '',
            new_repo_path: '',
        }),
        // TODO: use constant!
        computed: mapState('blame_manager', [
            'repos',
            'range_ref',
            'commit_limit',
            'commit_offset',
            'ext_whitelist',
        ]),
        methods: {
            // setRangeRef(evt) {
            //     this.$store.commit('blame_manager/' + SET_RANGE_REF, evt.target.value)
            // },
            setCommitLimit(evt) {
                this.$store.commit('blame_manager/' + SET_COMMIT_LIMIT, evt.target.value)
            },
            setCommitOffset(evt) {
                this.$store.commit('blame_manager/' + SET_COMMIT_OFFSET, evt.target.value)
            },
            add_repo() {
                const {repos} = this.$store.state.blame_manager
                const {
                    new_repo_name: name,
                    new_repo_path: path,
                    new_repo_url: url,
                } = this
                this.$store.commit('blame_manager/' + ADD_REPO, {...repos, [name]: {name, path, url}})
                this.new_repo_name = ''
                this.new_repo_path = ''
                this.new_repo_url = ''
            },
            delete_repo(name) {

                this.$store.commit('blame_manager/' + DEL_REPO, name)
            },
            // TODO: make an action instead!
            ...mapMutations('blame_manager', [
                SET_RANGE_REF,
                SET_EXT_WLIST,
            ]),
            ...mapActions('blame_manager', [
                BLAME_REPO,
            ])
        }
    }
</script>