<template>
  <header>
      <v-app-bar
        color="#6A76AB"
        dark
        shrink-on-scroll
        prominent
        src="https://picsum.photos/1920/1080?random"
        fade-img-on-scroll
        scroll-target="#scrolling-techniques-4"
      >
        <template v-slot:img="{ props }">
          <v-img
            v-bind="props"
            gradient="to top right, rgba(19,84,122,.5), rgba(128,208,199,.8)"
          ></v-img>
        </template>

        <v-toolbar-title>写真あげMASKぁ～？？</v-toolbar-title>

        <v-spacer></v-spacer>

        <v-btn icon>
          <v-icon>mdi-magnify</v-icon>
        </v-btn>

        <v-btn icon>
          <v-icon>mdi-heart</v-icon>
        </v-btn>

        <v-btn icon>
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>

        <template v-slot:extension>
            <v-tabs align-with-title>
              <v-tab router-link to="/" id="nav">Home</v-tab>
              <v-tab router-link to="/upload" id="nav">MASK</v-tab>
            </v-tabs>
          </template>
      </v-app-bar>
  </header>
</template>

<script>
  import constants from '../common/constants.js'
  export default {
    name: 'AppHeader',
    data () {
      return {
        drawer: false,
        menuItems: constants.menuItems
      }
    }
  }
</script>

<style>
  #nav {
    padding: 30px;
  }
  #nav a {
    font-weight: bold;
    color: #2c3e50;
  }
  #nav a.router-link-exact-active {
    color: #42b983;
  }
</style>