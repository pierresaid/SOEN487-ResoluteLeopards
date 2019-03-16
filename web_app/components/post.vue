<template>
  <div style="display:flex; align-items:center; flex-direction:column" class="box">
    <h1 class="title">{{post.title}}</h1>
    <div style="display:flex; flex-direction:column;">
      <div style="display:flex; flex-direction:row; justify-content: space-between; width:100%">
        <img
          :src="post.url_one"
          style="width:49%; height:400px; background-color:blue; border-radius: 5px;"
        >
        <img
          :src="post.url_two"
          style="width:49% ; height:400px; background-color:red; border-radius: 5px"
        >
      </div>
      <div
        style="width:100%; height:100%; display:flex; flex-direction:row; justify-content: space-between"
      >
        <i class="far fa-thumbs-up"/>
        <i class="far fa-thumbs-up"/>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    post: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
</style>
