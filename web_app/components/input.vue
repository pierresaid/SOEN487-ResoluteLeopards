<template>
  <p v-if="icon" class="control has-icons-left">
    <b-input v-bind="$attrs" v-on="$listeners"/>
    <span class="icon is-small is-left">
      <fa :icon="icon" style="color:black"/>
    </span>
  </p>
  <b-input placeholder="azd" v-else/>
</template>

<script>
export default {
  props: ['icon'],
  inheritAttrs: false
}
</script>

<style scoped>
</style>
