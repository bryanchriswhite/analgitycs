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
          <v-btn color="green darken-1" text @click="trackRepo">Submit</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
    import gql from 'graphql-tag';

    export default {
        name: 'Repos',
        apollo: {
            repos: gql`query{repos {
                key,
                rev,
                name,
                url
            }}`
        },
        data: () => ({
            dialog: false,
            repoName: '',
            repoURL: '',
        }),
        methods: {
            async trackRepo() {
                const {repoName: name, repoURL: url} = this;
                const {data: {trackRepo}} = await this.$apollo.mutate({
                    mutation: gql`mutation ($name: String!, $url: String!) {
                        trackRepo(name: $name, url: $url) {
                            name,
                            url,
                        }
                    }`,
                    variables: {
                        name,
                        url
                    }
                })
                if (trackRepo.ok) {
                    this.dialog = false;
                }
            },
            async deleteRepo(key) {
                const {data: {deleteRepo}} = await this.$apollo.mutate({
                    mutation: gql`mutation ($key: Int!) {
                        deleteRepo(key: $key) {ok}
                    }`,
                    variables: {
                        key
                    }
                })
                if (deleteRepo.ok) {
                    // TODO:
                }
            }
        }
    }
</script>
