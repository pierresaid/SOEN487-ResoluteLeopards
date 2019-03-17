<template>
  <div
    style="display:flex; align-items:center; flex-direction:column; max-width: 1100px;"
    class="box is-dark"
  >
    <h1 class="title">{{post.title}}</h1>
    <div style="display:flex; flex-direction:column;">
      <div style="display:flex; flex-direction:row; justify-content: space-between; width:100%">
        <img class="post-picture" :src="post.url_one">
        <img class="post-picture" :src="post.url_two">
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

<style  scoped>
.post-picture {
  width: 49%;
  height: 400px;
  border-style: solid;
  border-radius: 5px;
  border-width: 1px;
  padding: 10px;
  border-color: grey;
  cursor: pointer;
  user-select: none;
  -moz-user-select: none;
  -webkit-user-drag: none;
  -webkit-user-select: none;
  -ms-user-select: none;
}

.post-picture:hover {
  background-color: #b2fab4;
}
</style>
