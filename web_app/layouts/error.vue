<template>
  <div class="full-center">
    <h1 v-if="error.statusCode === 404" class="title is-1">Page not found</h1>
    <h1 v-else class="title is-1">An error occurred</h1>
    <nuxt-link class="button is-primary" to="/">Home page</nuxt-link>
  </div>
</template>

<script>
import navbar from '~/components/navbar'
import appContainer from '~/components/appContainer'
import footer from '~/components/footer'

export default {
  components: {
    'main-navbar': navbar,
    appContainer,
    'footer-section': footer
  },
  props: {
    error: {
      type: Number,
      default: undefined
    }
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
