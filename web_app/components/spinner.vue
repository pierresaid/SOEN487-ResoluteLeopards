<template>
  <half-circle-spinner
    v-if="!background"
    :animation-duration="1000"
    :size="60"
    :color="theme === 'dark' ? 'white' : 'black'"
  />
  <div v-else class="circle-background" :class="theme">
    <half-circle-spinner
      :animation-duration="1000"
      :size="60"
      :color="theme === 'dark' ? 'white' : 'black'"
    />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { HalfCircleSpinner } from 'epic-spinners/dist/lib/epic-spinners.min.js'
import 'epic-spinners/dist/lib/epic-spinners.min.css'

export default {
  components: {
    HalfCircleSpinner
  },
  props: {
    background: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    ...mapState({
      theme: state => state.user.theme
    })
  }
}
</script>

<style scoped>
.circle-background {
  width: 80px;
  height: 80px;
  border-radius: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
