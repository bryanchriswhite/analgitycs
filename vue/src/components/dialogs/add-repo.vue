<template>
  <v-dialog v-model="open" persistent max-width="290">
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
        <v-btn color="green darken-1" text @click="open = false">Cancel</v-btn>
        <v-btn color="green darken-1" text @click="trackRepo">Submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
    import {TrackRepoMutation} from "@/graphql/mutations";
    import REPOS_QUERY from '@/graphql/queries'

    export default {
        name: 'AddRepoDialog',
        data: () => ({
            open: false,
            repoName: '',
            repoURL: '',
        }),
        methods: {
            async trackRepo() {
                const {repoName: name, repoURL: url} = this;
                const {data: {trackRepo}} = await this.$apollo.mutate({
                    mutation: TrackRepoMutation,
                    update: (store, {data: {trackRepo}}) => {
                        const data = store.readQuery({query: REPOS_QUERY})
                        data.repos.push(trackRepo.repo)
                        store.writeQuery({query: REPOS_QUERY, data})
                    },
                    optimisticResponse: {
                        trackRepo: {
                            __typename: 'Mutation',
                            repo: {
                                __typename: 'Repo',
                                key: '-1',
                                rev: '',
                                name,
                                url
                            }
                        }
                    },
                    variables: {
                        name,
                        url
                    }
                })
                if (trackRepo.repo) {
                    this.open = false;
                    this.repoName = ''
                    this.repoURL = ''
                }
            }
        }
    }
</script>