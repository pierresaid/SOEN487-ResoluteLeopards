<template>
  <div>
    <h1>User index</h1>
    {{name}}
    <button @click="changeName('lel')">Hey</button>
    {{counter}}
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex'

export default {
  data() {
    return {
      counter: 0
    }
  },
  computed: {
    ...mapState({ name: state => state.user.name })
  },
  methods: {
    lol() {
      this.counter += 1
    },
    ...mapMutations({
      changeName: 'user/changeName'
    })
  }
}
</script>

<style scoped>
</style>
