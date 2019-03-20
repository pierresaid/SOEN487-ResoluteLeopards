<template>
  <p v-if="icon" class="control has-icons-left">
    <b-input v-bind="$attrs" v-on="$listeners"/>
    <span class="icon is-small is-left">
      <fa :icon="icon" style="color:black"/>
    </span>
  </p>
  <b-input v-else v-bind="$attrs" v-on="$listeners"/>
</template>

<script>
export default {
  inheritAttrs: false,
  props: {
    icon: {
      type: String,
      default: undefined
    }
  }
}
</script>

<style scoped>
</style>
