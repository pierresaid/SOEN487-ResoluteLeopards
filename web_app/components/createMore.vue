<template>
  <div class="box post" :class="theme">
    <h2 style="color:#adadad" class="subtitle">End of posts</h2>
    <button
      class="addmore notheme button is-outlined is-inverted"
      :class="'is-' + theme"
      @click="goToCreate"
    >
      <p>Create More !</p>
    </button>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState({
      theme: state => state.user.theme
    })
  },
  methods: {
    goToCreate() {
      this.$nuxt.$router.replace({ path: '/NewPost' })
    }
  }
}
</script>

<style scoped>
.addmore.is-dark:hover p,
.addmore.is-dark:focus p {
  color: black;
}
</style>
