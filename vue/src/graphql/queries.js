import gql from "graphql-tag";

export const REPOS_QUERY = gql`
query{repos{
    key, rev, name, url
}}`

