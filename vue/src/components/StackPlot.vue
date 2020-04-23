<template>
    <svg :viewBox="viewbox"></svg>
</template>

<script>
    import * as d3 from 'd3';

    export default {
        name: 'StackPlot',
        props: ['layers'],
        data() {
            return {
                // viewbox: "0 0 0 0",
                color_count: 10,
            }
        },
        computed: {
            viewbox() {
                return `0 0 ${this.$store.state.xMax} ${this.$store.state.yMax}`
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

                const stack = d3.layout.stack()
                const area = d3.svg.area()
                    .x(d => d.x)
                    .y0(d => d.y0)
                    .y1(d => d.y + d.y0)


                // const that = this
                // p.then(res => {
                //     if (typeof (res.error) != "undefined") {
                //         console.error(res.error)
                //         return
                //     }
                //     if (typeof (res.msg) != "undefined") {
                //         console.log(res.msg)
                //         return
                //     }

                const input_layers = layers.map(layer => {
                    return layer.map((n, i) => {
                        return {x: i * 50, y: n, y0: 0,}
                    })
                })
                const stacked_layers = stack(input_layers)
                const xMax = stacked_layers[0].length
                const yMax = d3.max(stacked_layers[stacked_layers.length - 1].map(n => n.y + n.y0))

                this.xMax = xMax
                this.yMax = yMax
                // this.setViewBox({xMax, yMax})

                d3.select('svg')
                    // .attr('viewBox', `0 0 ${xMax} ${yMax}`)
                    .selectAll('path')
                    .data(stacked_layers)
                    .enter().append('path')
                    .attr('class', (_, i) =>
                        `color-${i % this.color_count}`)
                    // .attr('fill', (_, i) => colors[i % colors.length])
                    .attr('stroke', 'none')
                    .attr('d', (d) => area(d))
                // })
            }
        }
    }
</script>

<style lang="stylus">
    // TODO: delete!
    body
        background-colorred;

    for num in 0..9%
        {'.color-' + num}
            fill hsl(num * 15, 60%, 50%)

</style>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="stylus">
    #d3-debug
        display none

    svg
        width 100vw
        height 100vh
        transform scaleY(-1)

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
