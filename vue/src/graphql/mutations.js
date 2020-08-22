import gql from "graphql-tag";

export const TrackRepoMutation = gql`
mutation ($name: String!, $url: String!) {
    trackRepo(name: $name, url: $url) {
      repo {
          key, rev, name, url
      }
    }
}`
