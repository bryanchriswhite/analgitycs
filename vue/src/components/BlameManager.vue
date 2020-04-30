<template>
    <section class="blame-manager">
        <h2>Blame Manager</h2>
        <section class="blame-params">
            <label>
                <span>range ref:</span>
                <input name="range_ref"
                       type="text"
                       placeholder="(e.g. master, a1b2c3, v1.0)"
                       @change="set_range_ref"
                       :value="range_ref"/>
            </label>
            <label>
                <span>commit limit:</span>
                <input name="commit_limit"
                       type="text"
                       @change="set_commit_limit"
                       :value="commit_limit"/>
            </label>
            <label>
                <span>max worktrees:</span>
                <input name="max_worktrees"
                       type="text"
                       placeholder="max worktrees"
                       @change="set_max_worktrees"
                       :value="max_worktrees"/>
            </label>
            <label>
                <span>max workers:</span>
                <input name="max_workers"
                       type="text"
                       placeholder="max workers"
                       @change="set_max_workers"
                       :value="max_workers"/>
            </label>
            <label>
                <span>ext whitelist:</span>
                <input name="ext_whitelist"
                       type="text"
                       placeholder="file ext whitelist"
                       @change="set_ext_whitelist"
                       :value="ext_whitelist"/>
            </label>
            <!--            <input name="commit_offset"-->
            <!--                   type="text"-->
            <!--                   placeholder="commit offset"-->
            <!--                   @change="setCommitOffset"-->
            <!--                   :value="commit_offset"/>-->
        </section>
        <section class="repo-params">
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
            <button @click="addRepo">+</button>
        </section>
        <section class="repos">
            <section class="repo" v-for="repo in repos" :key=repo.name>
                <blame-log :repo_name="repo.name"></blame-log>
                <button @click="clearBlame(repo.name)">Clear</button>
                <button @click="checkBlame(repo.name)">Check</button>
                <button @click="blameRepo(repo.name)">Blame</button>
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

    .blame-manager
        position absolute
        z-index 200
        top 0
        margin 0 auto
        width 100vw

    .blame-params
        label
            /*input*/
            display block
            /*text-align left*/
            margin 5px auto
</style>

<script>
    import {mapState, mapMutations, mapActions} from 'vuex';

    import BlameLog from '@/components/BlameLog';

    import {
        ADD_REPO,
        DEL_REPO,
        SET_RANGE_REF,
        SET_COMMIT_LIMIT,
        SET_COMMIT_OFFSET,
        SET_MAX_WORKTREES,
        SET_MAX_WORKERS,
        SET_EXT_WLIST,
        BLAME_REPO,
        DEL_BLAME,
        CHECK_BLAME,
    } from '@/store/blame_manager'

    export default {
        name: 'BlameManager',
        components: {
            BlameLog,
        },
        data: () => ({
            new_repo_name: '',
            new_repo_url: '',
            new_repo_path: '',
        }),
        // TODO: use constant?
        computed: mapState('blame_manager', [
            'repos',
            'range_ref',
            'commit_limit',
            'commit_offset',
            'max_worktrees',
            'max_workers',
            'ext_whitelist',
            'blames',
        ]),
        methods: {
            repoKey(name) {
                // const blamed = _.some(this.blames, k => k == name)
                // return `${name}${blamed ? '+' : '-'}`
                if (!this.repos[name]) return
                if (!this.blames[name]) return

                return `${name}-${this.blames[name].recent.length}`
            },
            checkBlame(name) {
                console.log('methods called')
                this.$store.dispatch('blame_manager/' + CHECK_BLAME, name)
            },
            // TODO: remove!
            clearBlame(name) {
                const that = this;
                this.$store.dispatch('blame_manager/' + DEL_BLAME, name).then(() => {
                    console.log('done 1...')
                    that.$forceUpdate();
                }, () => {
                    console.log('error 1')
                });
            },
            blameRepo(evt) {
                const that = this;
                this.$store.dispatch('blame_manager/' + BLAME_REPO, evt).then(() => {
                    console.log('done 2...')
                    that.$forceUpdate();
                }, () => {
                    console.log('error 2')
                });
            },
            addRepo() {
                const {
                    new_repo_name: name,
                    new_repo_path: path,
                    new_repo_url: url,
                } = this
                this.$store.commit('blame_manager/' + ADD_REPO, {name, path, url})
                this.new_repo_name = ''
                this.new_repo_path = ''
                this.new_repo_url = ''
            },
            // TODO: make an action instead!
            ...mapMutations('blame_manager', [
                SET_RANGE_REF,
                SET_EXT_WLIST,
                SET_COMMIT_LIMIT,
                SET_COMMIT_OFFSET,
                SET_MAX_WORKTREES,
                SET_MAX_WORKERS,
                DEL_REPO,
            ]),
            ...mapActions('blame_manager', [
                // BLAME_REPO,
            ])
        }
    }
</script>