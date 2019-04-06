<template>
  <div style="position: relative;">
    <slot name="parent"/>
    <span
      v-if="active"
      class="on-top"
      style="display: flex; align-items: center; justify-content: center;"
    >
      <slot name="child"/>
    </span>
  </div>
</template>

<script>
export default {
  props: {
    active: {
      type: Boolean,
      default: true
    }
  }
}
</script>


<style scoped>
.on-top {
  position: absolute;
  top: 0px;
  left: 0px;
  width: 100%;
  height: 100%;
}
</style>
