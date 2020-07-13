<template>
  <v-container :fluid="true" class="repos">
    <v-row>
      <v-col
          v-for="repo in repos"
          :key="repo"
      >
        <v-card>
          <v-card-title>
            {{repo.name}}
          </v-card-title>
          <v-card-subtitle>
            {{repo.url}}
          </v-card-subtitle>
          <!--          <v-card-text>-->
          <!--            {{repo.description}}-->
          <!--          </v-card-text>-->
          <v-card-actions class="d-flex justify-space-between">
            <v-btn text>
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn text>
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-btn fab class="mt-3">
      <v-icon >mdi-plus-thick</v-icon>
    </v-btn>
    <!--        <blame-manager/>-->
    <!--        <blame-history/>-->
    <!--        <StackPlot :layers="layers" :authors="authors"/>-->
  </v-container>
</template>

<script>
    import {mapState, mapMutations} from 'vuex';
    // import gql from 'graphql-tag';

    import {SET_COLOR} from '@/store/theme';
    // import StackPlot from '@/components/StackPlot.vue';
    // import BlameManager from '@/components/BlameManager';
    // import BlameHistory from '@/components/blame_history'

    export default {
        name: 'Home',
        apollo: {
            // hello: gql`query{hello}`
        },
        components: {
            // BlameManager,
            // BlameHistory,
            // StackPlot,
        },
        data: () => ({
            repos: [
                {
                    name: 'storj/storj',
                    url: 'git@github.com:storj/storj'
                },
                {
                    name: 'storj/uplink-c',
                    url: 'git@github.com:storj/uplink-c'
                },
                {
                    name: 'storj/uplink',
                    url: 'git@github.com:storj/uplink'
                }
            ],
            // options: [
            //     {text: "Dark", value: "hsl(0,0%,24%)"},
            //     {text: "Light", value: "hsl(0,0%,96%)"}
            // ]
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
