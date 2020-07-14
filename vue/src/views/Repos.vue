<template>
  <v-container :fluid="true" class="repos">
    <v-row>
      <v-col
          v-for="repo in repos"
          :key="repo.name"
      >
        <v-card>
          <v-card-title>
            {{repo.name}}
          </v-card-title>
          <v-card-subtitle>
            {{repo.url}}
          </v-card-subtitle>
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
                v-model="repoName"
            />
            <v-text-field
                label="URL"
                v-model="repoURL"
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
  </v-container>
</template>

<script>
    // import {mapState} from 'vuex';
    import gql from 'graphql-tag';

    export default {
        name: 'Repos',
        apollo: {
            repos: gql`query{repos {
                name,
                url
            }}`
        },
        components: {
        },
        data: () => ({
            dialog: false,
            repoName: '',
            repoURL: '',
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
            // ...mapState('stackplot', [
            //     'layers',
            //     'authors',
            // ]),
        },
        methods: {
            async trackRepo() {
                const result = await this.$apollo.mutate({
                    mutation: gql``
                })
                return result
            }
        }
    }
</script>
