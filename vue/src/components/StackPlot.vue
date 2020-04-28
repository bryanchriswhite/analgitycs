<template>
    <section class="root">
        <section class="plot">
            <!--        <svg viewbox="0 0 150px 100px" style="border: 1px solid red; width: 300px; height: 200px;">-->
            <!--            <path d="M 0,0 m 50,25 v 100 h 100"></path>-->
            <!--        </svg>-->
            <svg class="stackplot" :viewBox="viewbox"></svg>
        </section>
        <section class="legend">
            <ul>
                <li v-for="author in authors" :key="author">
                    {{author}}
                </li>
            </ul>
        </section>
    </section>
</template>

<script>
    import * as d3 from 'd3';

    export default {
        name: 'StackPlot',
        props: ['layers', 'authors'],
        data() {
            return {
                // viewbox: "0 0 0 0",
                color_count: 10,
            }
        },
        computed: {
            viewbox() {
                return `0 0 ${this.$store.state.stackplot.xMax} ${this.$store.state.stackplot.yMax}`
            }
        },
        mounted() {
            this.drawStackPlot()
        },
        updated() {
            this.drawStackPlot()
        },
        methods: {
            drawStackPlot() {
                const layers = this.$props.layers
                if (!layers || layers.length === 0) {
                    return
                }

                const area = d3.svg.area()
                    .x(d => d.x)
                    .y0(d => d.y0)
                    .y1(d => d.y + d.y0)

                d3.select('svg.stackplot')
                    .selectAll('path')
                    .data(layers)
                    .enter().append('path')
                    .attr('class', (_, i) => `color-${i % this.color_count}`)
                    .attr('stroke', 'none')
                    .attr('d', (layer) => area(layer))
            }
        }
    }
</script>

<style lang="stylus">
    for num in 0..9%
        svg.stackplot path{'.color-' + num}
            fill hsl(num * 15, 60%, 50%)

</style>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="stylus">
    svg.stackplot
        width 100vw
        height 100vh
        transform scaleY(-1)

    /*width 1000px*/
    /*height 750px*/
    /*border 1px solid red*/

    h3
        margin 40px 0 0

    ul
        list-style-type none
        padding 0

    li
        display inline-block
        margin 0 10px

    a
        color #42b983
</style>
