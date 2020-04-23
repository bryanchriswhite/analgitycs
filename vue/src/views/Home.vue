<template>
    <div class="home">
        <ThemedBG :color="bgColor"/>
        <label for="theme">Theme:&nbsp;</label>
        <select name="theme" v-model="bgColor">
            <option v-for="option in options" :key="option.value" :value="option.value">
                {{option.text}}
            </option>
        </select>
        <StackPlot msg="Welcome to Your Vue.js App"/>
    </div>
</template>

<script>
    import {SET_COLOR} from '@/store/actions'
    import StackPlot from '@/components/StackPlot.vue'
    import ThemedBG from '@/components/ThemedBG.vue'

    export default {
        name: 'Home',
        components: {
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
                    return this.$store.state.color
                },
                set(value) {
                    this.$store.commit(SET_COLOR, value)
                }
            }
        },
    }
</script>
