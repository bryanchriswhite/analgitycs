<template>
    <div class="home">
        <ThemedBG :color="bgColor"/>
        <label>Theme:&nbsp;
            <select name="theme" v-model="bgColor">
                <option v-for="option in options" :key="option.value" :value="option.value">
                    {{option.text}}
                </option>
            </select>
        </label>
        <blame-manager/>
        <StackPlot :layers="layers"/>
    </div>
</template>

<script>
    import {SET_COLOR} from '@/store/theme';
    import {SET_LAYERS} from '@/store/stackplot';
    import StackPlot from '@/components/StackPlot.vue';
    import ThemedBG from '@/components/ThemedBG.vue';
    // import * as fetch from 'd3-fetch';
    import BlameManager from "../components/BlameManager";

    // TODO: something better!
    // const p = fetch.json('http://localhost:5000/repo/storj', {mode: 'cors'})

    export default {
        name: 'Home',
        components: {
            BlameManager,
            StackPlot,
            ThemedBG,
        },
        data: () => ({
            options: [
                {text: "Dark", value: "hsl(0,0%,24%)"},
                {text: "Light", value: "hsl(0,0%,96%)"}
            ]
        }),
        computed: {
            bgColor: {
                get() {
                    return this.$store.state.theme.color
                },
                set(value) {
                    this.$store.commit('theme/' + SET_COLOR, value)
                }
            },
            layers: {
                get() {
                    return this.$store.state.stackplot.layers
                },
                set(value) {
                    console.log(value)
                    this.$store.commit('stackplot/' + SET_LAYERS, value)
                }
            }
        },
        // TODO: something better!
        // beforeCreate() {
        //     const that = this
        //     p.then(({layers}) => {
        //         console.log(layers)
        //         that.layers = layers
        //     })
        // }
    }
</script>
