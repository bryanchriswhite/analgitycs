<template>
    <div>
        <div id="d3-debug"></div>
        <svg :viewBox="viewbox"></svg>
    </div>
</template>

<script>
    import * as d3 from 'd3';
    import * as fetch from 'd3-fetch';

    const p = fetch.json('http://localhost:5000/repo/storj', {mode: 'cors'})

    export default {
        name: 'HelloWorld',
        props: {
            msg: String
        },
        methods: {
            setViewBox({xMax, yMax}) {
                this.viewbox = `0 0 ${xMax} ${yMax}`
            }
        },
        data() {
            return {
                viewbox: "0 0 0 0",
                color_count: 10,
            }
        },
        mounted() {
            const stack = d3.layout.stack()
            const area = d3.svg.area()
                .x(d => d.x)
                .y0(d => d.y0)
                .y1(d => d.y + d.y0)


            const that = this
            p.then(res => {
                if (typeof (res.error) != "undefined") {
                    console.error(res.error)
                    return
                }
                if (typeof (res.msg) != "undefined") {
                    console.log(res.msg)
                    return
                }

                const layers = res.layers
                const input_layers = layers.map(layer => {
                    return layer.map((n, i) => {
                        return {x: i * 50, y: n, y0: 0,}
                    })
                })
                const stacked_layers = stack(input_layers)
                const xMax = stacked_layers[0].length
                const yMax = d3.max(stacked_layers[stacked_layers.length - 1].map(n => n.y + n.y0))
                // this.setState({xMax, yMax})
                console.log(that)
                this.setViewBox({xMax, yMax})
                console.log(input_layers)

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

                // d3.select('#d3-debug')
                //     .selectAll('div')
                //     .data(stack(layers))
                //     .enter().append('div')
                //     .text(d => {
                //         return `d: ${JSON.stringify(d)}`
                //     })
            })
        }
    }
</script>

<style lang="stylus">
    // TODO: delete!
    body
        background-colorred;

    for num in 0..9%
        {'.color-' + num}
            fill hsl(num*15, 60%, 50%)

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
