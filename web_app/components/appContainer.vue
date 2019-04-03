<template>
  <section class="section" :class="theme === 'light' ? 'background' : 'dark-background'">
    <div class="container" :class="'app-is-' + theme">
      <slot/>
    </div>
  </section>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState({
      theme: state => state.user.theme
    })
  }
}
</script>

<style scoped>
</style>
