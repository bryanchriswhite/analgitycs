<template>
  <v-container :fluid="true" class="repos">
    <v-row>
      <v-col
          v-for="repo in repos"
          :key="`${repo.key}${repo.rev}`"
          sm="12" md="6"
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
            <v-btn
                text
                @click="deleteRepo(repo.key)"
            >
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <AddRepoDialog/>
  </v-container>
</template>

<script>
    import gql from 'graphql-tag';
    import AddRepoDialog from '@/components/dialogs/add-repo'
    import {REPOS_QUERY} from '@/graphql/queries'

    export default {
        name: 'Repos',
        components: {
            AddRepoDialog,
        },
        apollo: {
            repos: REPOS_QUERY
        },
        methods: {
            async deleteRepo(key) {
                const deleteRepo = await this.$apollo.mutate({
                    mutation: gql`mutation ($key: Int!) {
                        deleteRepo(key: $key) {ok}
                    }`,
                    update: (store) => {
                        let data = store.readQuery({query: REPOS_QUERY})
                        const startIndex = data.repos.findIndex(r => r.key === key) - 1
                        data.repos.splice(startIndex, 1)
                        store.writeQuery({query: REPOS_QUERY, data})
                    },
                    variables: {
                        key
                    }
                })
                if (deleteRepo.ok) {
                    this.repoName = ''
                    this.repoURL = ''
                } else {
                    // TODO: error handling
                }
            }
        }
    }
</script>
