<template>
  <div class="box" :class="theme">
    <slot/>
  </div>
</template>

<script>
export default {
  computed: {
    theme() {
      return this.$store.state.user.theme
    }
  }
}
</script>
