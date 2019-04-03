<template>
  <div style="width:90%">
    <delimiter/>
    <div style="display:flex; justify-content: space-around;">
      <div style="display:flex; align-items:center">
        <transition :duration="100" name="fade" mode="out-in">
          <fa
            v-if="nbr === 1"
            key="1"
            class="heart"
            :icon="['far', 'heart']"
            @click="nbr = (nbr === 1 ? 0 : 1)"
          />
          <fa
            v-else
            key="2"
            class="heart"
            :icon="['fas', 'heart']"
            @click="nbr = (nbr === 1 ? 0 : 1)"
          />
        </transition>
        <p>{{nbr}} votes</p>
      </div>
      <div style="display:flex; align-items:center">
        <transition :duration="100" name="fade" mode="out-in">
          <fa
            v-if="nbr === 1"
            key="1"
            class="heart"
            :icon="['far', 'heart']"
            @click="nbr = (nbr === 1 ? 0 : 1)"
          />
          <fa
            v-else
            key="2"
            class="heart"
            :icon="['fas', 'heart']"
            @click="nbr = (nbr === 1 ? 0 : 1)"
          />
        </transition>
        <p>{{nbr}} votes</p>
      </div>
    </div>
  </div>
</template>

<script>
import delimiter from './delimiter'

export default {
  components: {
    delimiter
  },
  data() {
    return {
      nbr: 1,
      show: true
    }
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.heart {
  color: #ff007e;
  width: 50px;
  height: 50px;
  margin: 10px;
  user-select: none;
  -moz-user-select: none;
  -webkit-user-drag: none;
  -webkit-user-select: none;
  -ms-user-select: none;
  cursor: pointer;
}
</style>
