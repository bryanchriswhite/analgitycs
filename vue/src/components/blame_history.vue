<template>
    <section>
        <svg viewBox="0 0 500 500">
            <path fill="none"
                  :d="line(selectedRepoBlames)">
            </path>
        </svg>
        <select :value="selectedRepo"
                @change="select_repo">
            <option v-for="(_, name) in blames"
                    :key="name"
                    :value="name">
                {{name}}
            </option>
        </select>
    </section>
</template>

<style scoped lang="stylus">
    svg
        width 500px
        height 500px

        path
            stroke #93ffbe
            stroke-width 5
            stroke-linejoin round
            stroke-linecap round


</style>

<script>
    import {mapState, mapMutations} from 'vuex';
    import * as _ from 'lodash';
    import * as d3 from 'd3';

    import {SELECT_REPO} from "@/store/blame_history";

    export default {
        name: 'BlameHistory',
        data: () => ({
            // ...
        }),
        computed: {
            selectedRepoBlames() {
                if (!this.blames || !this.blames[this.selectedRepo]) return [];
                const _selectedBlames = this.blames[this.selectedRepo];
                let blames = [];
                if (!!_selectedBlames.recent && _selectedBlames.recent.length) {
                    blames = _selectedBlames.recent;
                }
                if (this.blames.last) {
                    blames.push(this.blames.last);
                }

                return blames.slice().reverse();
            },
            scaleX: {
                get() {
                    return 1 / 1;
                },
            },
            scaleY: {
                get() {
                    return 1 //1 / 1;
                },
            },
            ...mapState('blame_manager', [
                'blames',
            ]),
            ...mapState('blame_history', [
                'selectedRepo',
            ])
        },
        methods: {
            line(blames) {
                if (!blames || !blames.length) return;
                blames = _.compact(blames);
                blames = _.sortBy(blames, n => parseInt(n.params.commit_limit, 10));
                console.log(_.map(blames, n => [n.params.commit_limit, n.result.status.end - n.result.status.start]));

                const _line = d3.svg.line()
                    .x(d => d ? d.params.commit_limit * this.scaleX : 0)
                    .y(d => d ? d.result.status.end - d.result.status.start * this.scaleY : 0)
                ;


                // const point = {
                //     x: blame.params.commit_limit,
                //     y: blame.result.status.end - blame.result.status.start,
                // }
                return _line(blames);
            },
            blameHistory(name) {
                const blame = this.blames[name]
                if (!blame || !blame.recent) return
                return _.compact(blame.recent)
            },
            ...mapMutations('blame_history', [
                SELECT_REPO,
            ])
        },
    }
</script>