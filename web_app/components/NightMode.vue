<template>
  <div>
    <transition name="fade" once mode="out-in">
      <div v-if="theme === 'light'" class="button is-light" @click="toggleTheme">
        <transition name="rotate" appear>
          <fa icon="moon"/>
        </transition>
      </div>
      <button v-else class="button is-dark" @click="toggleTheme">
        <transition name="rotate" appear>
          <fa icon="sun" style="color:yellow"/>
        </transition>
      </button>
    </transition>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex'

export default {
  computed: {
    ...mapState({ theme: state => state.user.theme })
  },
  methods: {
    ...mapMutations({ toggleTheme: 'user/toggleTheme' })
  }
}
</script>

<style scoped>
.rotate-enter-active,
.rotate-leave-active {
  transition: all 1.3s ease;
}
.rotate-enter,
.rotate-leave-to {
  transform: rotateZ(360deg);
}
</style>
