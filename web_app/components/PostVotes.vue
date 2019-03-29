<template>
  <div style="width:90%">
    <delimiter/>
    <div style="display:flex; justify-content: space-around;">
      <div style="display:flex; align-items:center">
        <img class="heart" src="~/assets/heart.png">
        <p>{{nbr}} votes</p>
      </div>
      <div style="display:flex; align-items:center">
        <img class="heart" src="~/assets/heart.png" @click="nbr += 1">
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
      nbr: 1
    }
  }
}
</script>

<style scoped>
.heart {
  width: 50px;
  height: 50px;
  margin: 10px;
}
</style>
