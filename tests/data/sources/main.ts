
const test = useQuery({
  query: /* GraphQL */ `
    query {
      currentUser {
        username
      }
    }
`})

const test2 = useQuery({
  query: /* GraphQL */ `
    query {
      currentUser {
        email
      }
    }
`})
