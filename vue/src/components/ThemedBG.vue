<template>
    <div class="themed-bg" :style="style" :data-color="color"/>
</template>

<script>
    export default {
        name: 'ThemedBG',
        props: ['color'],
        computed: {
            style() {
                return `background-color: ${this.$props.color}`
            }
        },
        mounted() {
            console.log(this.$props)
        }
        // computed: {
        //     style() {
        //         return `background-color: ${this.color}`
        //     }
        // }
    }
</script>

<style scoped lang="stylus">
    .themed-bg
        // TODO: ?
        /*display flex*/
        position absolute
        top 0
        left 0
        width 100vw
        height 100vh
        z-index -100
</style>