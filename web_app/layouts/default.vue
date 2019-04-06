<template>
  <div>
    <no-ssr>
      <main-navbar/>
    </no-ssr>
    <app-container>
      <nuxt/>
    </app-container>

    <footer-section/>
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
@import '~/assets/style.css';
</style>
