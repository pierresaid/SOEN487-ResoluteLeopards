<template>
  <div :class="'delimiter-' + theme"/>
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
.delimiter-dark {
  width: 100%;
  border-bottom: solid white 1px;
  margin: 15px;
}

.delimiter-light {
  width: 100%;
  border-bottom: solid black 1px;
  margin: 15px;
}
</style>
