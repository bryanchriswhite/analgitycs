<template>
    <section class="root">
        <section class="plot">
            <!--        <svg viewbox="0 0 150px 100px" style="border: 1px solid red; width: 300px; height: 200px;">-->
            <!--            <path d="M 0,0 m 50,25 v 100 h 100"></path>-->
            <!--        </svg>-->
            <svg class="stackplot" :viewBox="viewbox">
                <path v-for="(layer, i) in layers"
                      stroke="none"
                      @mouseenter="set_active_layer(i)"
                      @mouseleave="set_active_layer(null)"
                      :key="JSON.stringify([i,active_layer])"
                      :class="colorClass(i)"
                      :d="pathArea(layer)"
                ></path>
            </svg>
        </section>
        <section class="legend">
            <ul>
                <li v-for="(author, i) in authors.slice().reverse()"
                    :key="author">
                    <i :class="colorClass(authors.length - 1 - i)"></i>
                    <span>{{author}}</span>
                </li>
            </ul>
        </section>
    </section>
</template>

<style lang="stylus">
    for num in 0..9%
        .legend i.color-{num}
            background-color hsl(num * 15, 60%, 50%)

        .stackplot path.color-{num}
                fill hsl(num * 15, 60%, 50%)

    .stackplot path
        &[class^="color-fade-"]
            fill #dbdbdb

        for num in 0..2%
            &.color-fade-{num}
                fill hsl(0, 50%/num, 70%/num)



</style>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="stylus">
    .stackplot path.color-highlight
        fill #ea4cb4

    svg.stackplot
        width 100vw
        height 100vh
        transform scaleY(-1)

    .legend
        position fixed
        left 25px
        bottom 25px

        ul
            list-style none

            li
                text-align left
                margin 0 0 5px 0

                i
                    display inline-block
                    width 10px
                    height 10px
                    margin-right 5px

    /*width 1000px*/
    /*height 750px*/
    /*border 1px solid red*/
</style>

<script>
    import {mapState, mapMutations} from 'vuex';
    import * as d3 from 'd3';

    // import {SET_ACTIVE_LAYER} from '@/store/stackplot';

    const area = d3.svg.area()
        .x(d => d.x)
        .y0(d => d.y0)
        .y1(d => d.y + d.y0)

    export default {
        name: 'StackPlot',
        props: ['layers', 'authors'],
        data() {
            return {
                // viewbox: "0 0 0 0",
                color_count: 10,
                active_layer: null,
            }
        },
        computed: {
            viewbox() {
                return `0 0 ${this.$store.state.stackplot.xMax} ${this.$store.state.stackplot.yMax}`
            },
            ...mapState('stackplot', [
                // 'active_layer',
            ]),
        },
        // mounted() {
        //     this.drawstackplot()
        // },
        // updated() {
        //     this.drawstackplot()
        // },
        methods: {
            // highlightLayer(i) {
            //     const layers = this.$props.layers
            //     if (!layers || layers.length === 0) {
            //         return
            //     }
            //
            //     // d3.select('svg.stackplot')
            //     //     .selectAll('path')
            //     //     .data(layers)
            //     //     .enter().forEach( => {
            //     //         layer
            //     //     // .attr('class', (_, j) => i == j ? 'highlight' : '')
            //     // })
            //
            // },
            pathArea(layer) {
                return area(layer)
            },
            colorClass(i) {
                if (this.active_layer === i) {
                    return 'color-highlight';
                } else if (this.active_layer !== null) {
                    const j = Math.abs(i - this.active_layer);
                    return `color-fade-${j}`;
                }
                return `color-${i % this.color_count}`
            },
            set_active_layer(layer_index) {
                this.active_layer = layer_index;
            },
            // drawStackPlot() {
            //     // const layers = this.$props.layers
            //     // if (!layers || layers.length === 0) {
            //     //     return
            //     // }
            //
            //     // d3.select('svg.stackplot')
            //     //     .selectAll('path')
            //     //     .data(layers)
            //     //     .enter().append('path')
            //     //     .attr('class', (_, i) => `color-${i % this.color_count}`)
            //     //     .attr('stroke', 'none')
            //     //     .attr('d', (layer) => area(layer))
            // },
            ...mapMutations('stackplot', [
                // SET_ACTIVE_LAYER,
            ]),
        }
    }
</script>
