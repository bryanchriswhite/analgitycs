<template>
    <section class="root">
        <section class="plot">
            <!--                    <svg viewBox="0 0 150 100" style="border: 1px solid red; width: 300px; height: 200px;">-->
            <!--                        <path d="M 0,0 m 50,25 v 100 h 100"></path>-->
            <!--                    </svg>-->
            <svg class="stackplot"
                 preserveAspectRatio="xMinYMin slice"
                 :viewBox="viewbox"
                 :data-active-layer="active_layer">
                <path v-for="(layer, i) in layers"
                      stroke="none"
                      @mouseenter="set_active_layer(i)"
                      @mouseleave="set_active_layer(null)"
                      :key="JSON.stringify([i,scaleX,scaleY])"
                      :class="colorClass(i)"
                      :d="pathArea(layer)"
                ></path>
            </svg>
            <section>
                <input type="range" max="128" min="1" v-model="scaleX" />
                <input type="range" max="50" min="1" v-model="scaleY" />
            </section>
        </section>
        <section class="legend">
            <ul>
                <li v-for="(author, i) in sortedAuthors"
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

        .stackplot
            path.color-{num}, path.color-{num}:hover
                fill hsl(num * 15, 60%, 50%)


</style>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="stylus">
    svg.stackplot
        /*width 100vw*/
        /*height 100vh*/
        //transform scaleY(-1)

        width 1000px
        height 1000px
        transform scale(1, -1)
        border 1px solid red

        path
            transition fill 500ms

        /*&:hover path
            fill hsl(0, 0%, 85%)*/

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
</style>

<script>
    import * as d3 from 'd3';

    export default {
        name: 'StackPlot',
        props: ['layers', 'authors'],
        data() {
            return {
                scaleX: 1,
                scaleY: 1,
                color_count: 10,
                active_layer: null,
            }
        },
        computed: {
            viewbox() {
                return `0 0 ${this.$store.state.stackplot.xMax * 2} ${this.$store.state.stackplot.yMax}`
            },
            sortedAuthors() {
                if (!this.authors) return [];
                return this.authors.slice().reverse()
            },
        },
        methods: {
            pathArea(layer) {
                const area = d3.svg.area()
                    .x(d => d.x * (this.scaleX / 50))
                    .y0(d => d.y0 * (1 / this.scaleY))
                    .y1(d => (d.y * (1 / this.scaleY)) + (d.y0 * (1 / this.scaleY)))

                return area(layer)
            },
            colorClass(i) {
                if (this.active_layer === null || this.active_layer === i) {
                    return `color-${i % this.color_count}`
                }
                return 'color-fade'
            },
            set_active_layer(layer_index) {
                this.active_layer = layer_index;
            },
        }
    }
</script>
