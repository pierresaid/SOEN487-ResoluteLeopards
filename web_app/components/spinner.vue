<template>
  <half-circle-spinner
    :animation-duration="1000"
    :size="60"
    :color="theme === 'dark' ? 'white' : 'black'"
  />
</template>

<script>
import { mapState } from 'vuex'
// import { HalfCircleSpinner } from 'epic-spinners'
import { HalfCircleSpinner } from 'epic-spinners/dist/lib/epic-spinners.min.js'
import 'epic-spinners/dist/lib/epic-spinners.min.css'

export default {
  components: {
    HalfCircleSpinner
  },
  computed: {
    ...mapState({
      theme: state => state.user.theme
    })
  }
}
</script>

<style scoped>
</style>
