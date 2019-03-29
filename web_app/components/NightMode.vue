<template>
  <div>
    <transition name="fade" once mode="out-in">
      <div v-if="theme === 'light'" class="button moon-button is-light" @click="toggleTheme">
        <transition name="rotate" appear>
          <fa class="moon" icon="moon"/>
        </transition>
      </div>
      <button v-else class="button is-dark sun-button" @click="toggleTheme">
        <transition name="rotate" appear>
          <fa class="sun" icon="sun" style="color:yellow"/>
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

.sun-button:hover .sun {
  -webkit-animation-name: rotate;
  -webkit-animation-duration: 2s;
  -webkit-animation-iteration-count: infinite;
  -webkit-animation-timing-function: linear;
  -moz-animation-name: rotate;
  -moz-animation-duration: 2s;
  -moz-animation-iteration-count: infinite;
  -moz-animation-timing-function: linear;
  animation-name: rotate;
  animation-duration: 2s;
  animation-iteration-count: infinite;
  animation-timing-function: linear;
}

@-webkit-keyframes rotate {
  from {
    -webkit-transform: rotate(0deg);
  }
  to {
    -webkit-transform: rotate(360deg);
  }
}

.moon-button:hover .moon {
  -webkit-animation-name: color-shift;
  -webkit-animation-duration: 2s;
  -webkit-animation-iteration-count: infinite;
  -webkit-animation-timing-function: linear;
  -moz-animation-name: color-shift;
  -moz-animation-duration: 2s;
  -moz-animation-iteration-count: infinite;
  -moz-animation-timing-function: linear;
  animation-name: color-shift;
  animation-duration: 2s;
  animation-iteration-count: infinite;
  animation-timing-function: linear;
}

@-webkit-keyframes color-shift {
  0% {
    color: black;
  }
  50% {
    color: rgb(199, 197, 197);
  }
  100% {
    color: black;
  }
}
</style>
