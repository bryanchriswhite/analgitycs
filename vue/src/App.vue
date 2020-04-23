<template>
  <div id="app">
<!--    <div id="nav">-->
<!--      <router-link to="/">Home</router-link> |-->
<!--      <router-link to="/about">About</router-link>-->
<!--    </div>-->
    <router-view/>
  </div>
</template>

<style lang="stylus">
#app
  font-family Avenir, Helvetica, Arial, sans-serif
  -webkit-font-smoothing antialiased
  -moz-osx-font-smoothing grayscale
  text-align center
  color #2c3e50
  /*margin-top 50px*/
</style>

<style scoped lang="stylus">
  #nav
    position absolute
    top 0
    left 0
    width 100vw
    height 50px

    // TODO: something else
    pointer-events none
    &>*
      pointer-events all
</style>
