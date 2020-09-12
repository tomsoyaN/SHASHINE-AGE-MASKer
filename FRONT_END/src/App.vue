<template>
  <v-app>
    <AppHeader/>
    <v-scroll-x-transition mode="in" hide-on-leave="true">
        <router-view></router-view>
    </v-scroll-x-transition>
  <v-footer color="primary" dark app>
    Cos5year
  </v-footer>
  </v-app>
</template>

<script>
import AppHeader from './components/AppHeader.vue'
export default {
  name: 'App',

  components: {
    AppHeader
  },

  data: () => ({
    drawer: false
  }),
};
</script>

<style scoped>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }
</style>