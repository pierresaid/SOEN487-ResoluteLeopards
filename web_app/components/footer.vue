<template>
  <footer class="footer" :class="theme">
    <div class="content has-text-centered">
      <p>
        <strong>Cat vs Dog</strong> by the ResoluteLeopards for the SOEN487 Project
      </p>
    </div>
  </footer>
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
