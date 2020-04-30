<template>
    <ul class="blame-log">
        <li v-for="blame in blameHistory(repo_name)" :key="blame.start">
            <section v-if="!!blame" class="status">
                        <span>
                            {{statusDuration(blame.result.status)}}s
                        </span>
                <i :class="doneClass(blame.result.status)"></i>
                <i :class="errorClass(blame.result.status)"></i>
            </section>
        </li>
    </ul>
</template>

<style scoped lang="stylus">
    .blame-log
        display inline-block
        text-align right

    ul
        list-style none
        margin 0
        padding 0
        vertical-align text-top

        height 25px
        overflow hidden
        transition height 500ms

        &:hover
            height 100px
            overflow-y scroll

        &>li
            line-height 25px

    .status
        display inline-block

        i
            display inline-block
            width 20px
            height 20px

            &.pending
                background-color #eaa92f

            &.done
                background-color #30cb30

            &.error
                background-color #e74a4a
</style>

<script>
    import {mapState} from 'vuex';
    import * as _ from "lodash";

    export default {
        name: 'BlameLog',
        props: ['repo_name'],
        methods: {
            statusDuration(status) {
                if (!status || !status.start || !status.end) return
                const {start, end} = status;
                return _.round(end - start, 2)
            },
            blameHistory(name) {
                const blame = this.blames[name]
                if (!blame || !blame.recent) return
                return _.compact(blame.recent)
            },
            doneClass(status) {
                return status.done ? 'done' : 'pending'
            },
            errorClass(blame) {
                if (!blame || !blame.result) return
                const error = blame.result.status.error
                return (error && error !== 'None') ? 'error' : ''
            },
        },
        computed: {
            ...mapState('blame_manager', [
                'repos',
                'blames',
            ])
        }
    }
</script>
