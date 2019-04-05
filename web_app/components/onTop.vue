<template functional>
  <div style="position: relative;">
    <slot name="parent"/>
    <span class="on-top" style="display: flex; align-items: center; justify-content: center;">
      <slot name="child"/>
    </span>
  </div>
</template>

<style scoped>
.on-top {
  position: absolute;
  top: 0px;
  left: 0px;
  width: 100%;
  height: 100%;
}
</style>
