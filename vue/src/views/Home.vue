<template>
    <div class="home">
        <ThemedBG :color="bgColor"/>
        <label>Theme:&nbsp;
            <select name="theme"
                    @change="set_color"
                    :value="bgColor">
                <option v-for="option in options" :key="option.value" :value="option.value">
                    {{option.text}}
                </option>
            </select>
        </label>
        <blame-manager/>
        <blame-history/>
        <StackPlot :layers="layers" :authors="authors"/>
    </div>
</template>

<script>
    import {mapState, mapMutations} from 'vuex';

    import {SET_COLOR} from '@/store/theme';
    import StackPlot from '@/components/StackPlot.vue';
    import ThemedBG from '@/components/ThemedBG.vue';
    import BlameManager from '@/components/BlameManager';
    import BlameHistory from '@/components/blame_history'

    export default {
        name: 'Home',
        components: {
            BlameManager,
            BlameHistory,
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
            ...mapState('stackplot', [
                'layers',
                'authors',
            ]),
            ...mapState('theme', {
                bgColor: 'color',
            })
        },
        methods: mapMutations('theme', [SET_COLOR])
    }
</script>
