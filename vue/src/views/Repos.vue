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
    <v-dialog v-model="dialog" persistent max-width="290">
      <template v-slot:activator="{ on, attrs }">
        <v-btn
            fab
            class="mt-3"
            color="primary"
            dark
            v-bind="attrs"
            v-on="on"
        >
          <v-icon>mdi-plus-thick</v-icon>
        </v-btn>
      </template>
      <v-card>
        <v-card-title class="headline">Add a new repo</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field
                label="Name"
                v-model="newRepoName"
            />
            <v-text-field
                label="URL"
                v-model="newRepoURL"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="dialog = false">Cancel</v-btn>
          <v-btn color="green darken-1" text @click="dialog = false">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!--        <blame-manager/>-->
    <!--        <blame-history/>-->
    <!--        <StackPlot :layers="layers" :authors="authors"/>-->
  </v-container>
</template>

<script>
    import {mapState, mapMutations} from 'vuex';
    // import gql from 'graphql-tag';

    export default {
        name: 'Home',
        apollo: {
            // hello: gql`query{hello}`
        },
        components: {
        },
        data: () => ({
            dialog: false,
            newRepoName: '',
            newRepoURL: '',
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
        methods: {
            async addRepo() {
                const result = this.$apollo.mutate({
                    mutation: gql`mutation (`
                })
            }
        }
    }
</script>
