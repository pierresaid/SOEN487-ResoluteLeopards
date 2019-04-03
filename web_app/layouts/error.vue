<template>
  <div class="full-center">
    <h1 class="title is-1" v-if="error.statusCode === 404">Page not found</h1>
    <h1 class="title is-1" v-else>An error occurred</h1>
    <nuxt-link class="button is-primary" to="/">Home page</nuxt-link>
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

<style>
.full-center {
  display: flex;
  align-items: center;
  height: -webkit-fill-available;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
</style>
