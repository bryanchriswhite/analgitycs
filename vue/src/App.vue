<template>
  <v-app>
    <v-app-bar
        :clipped-left="true"
        app
        color="primary"
        dark
    >
      <v-btn text
             class="mr-3"
             v-on:click="toggleDrawer"
      >
        <v-icon>
          mdi-menu
        </v-icon>
      </v-btn>
      Analgitycs Viewer
    </v-app-bar>
    <v-navigation-drawer
        :app="true"
        :clipped="true"
        :permanent="true"
        :mini-variant="drawer"
        :width="150"
    >
      <v-list dense nav>
        <v-list-item>
          <v-list-item-icon class="mr-3">
            <v-icon>mdi-git</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <router-link to="/routes">
              Repos
            </router-link>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-icon class="mr-3">
            <v-icon>mdi-database-edit</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <router-link to="/orders">
              Orders
            </router-link>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>
    export default {
        name: 'App',
        // components: {
        // },
        data: () => ({
            drawer: false,
        }),
        methods: {
            toggleDrawer() {
                this.drawer = !this.drawer;
            },
        },
    };
</script>
