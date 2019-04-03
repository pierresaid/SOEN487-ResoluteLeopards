<template>
  <div>
    <h1 v-if="error.statusCode === 404">Page not found</h1>
    <h1 v-else>An error occurred</h1>
    <nuxt-link to="/">Home page</nuxt-link>
  </div>
</template>

<script>
import navbar from '~/components/navbar'
import appContainer from '~/components/appContainer'
import footer from '~/components/footer'

export default {
  props: ['error'],
  components: {
    'main-navbar': navbar,
    appContainer,
    'footer-section': footer
  },
  head() {
    return {
      titleTemplate: 'Cat VS Dog',
      meta: [
        {
          content: 'The only battle worth fighting'
        }
      ]
    }
  }
}
</script>
