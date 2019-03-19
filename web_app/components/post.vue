<template>
  <transition name="fade">
    <div v-show="loaded === 2" class="box post" :class="theme">
      <h1 class="title">{{post.title}}</h1>
      <div style="display:flex; flex-direction:column;">
        <div style="display:flex; flex-direction:row; justify-content: space-between; width:100%">
          <img class="post-picture" :src="post.url_one" @load="OnImgLoad">
          <img class="post-picture" :src="post.url_two" @load="OnImgLoad">
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { mapState } from 'vuex'

export default {
  props: {
    post: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      loaded: 0
    }
  },
  computed: {
    ...mapState({ theme: state => state.user.theme })
  },
  methods: {
    OnImgLoad() {
      this.loaded += 1
    }
  }
}
</script>

<style  scoped>
.post {
  display: flex;
  align-items: center;
  flex-direction: column;
  max-width: 1100px;
}
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
  background-color: white;
}

.post-picture:hover {
  background-color: #22c65b;
  border-color: #22c65b;
}
</style>
