<template>
  <transition name="fade">
    <div v-show="loaded === 2" class="box post" :class="theme">
      <h1 class="title">{{post.title}}</h1>
      <h2 class="subtitle">Subtitle</h2>
      <div style="display:flex; flex-direction:column;">
        <div style="display:flex; flex-direction:row; justify-content: space-between; width:100%">
          <img
            class="post-picture"
            :class="{'voted' : post.user_vote === 0}"
            :src="post.url_one"
            @load="OnImgLoad"
            @click="clickVote(0)"
          >
          <img
            class="post-picture"
            :class="{'voted' : post.user_vote === 1}"
            :src="post.url_two"
            @load="OnImgLoad"
            @click="clickVote(1)"
          >
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { mapState, mapActions } from 'vuex'

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
    ...mapActions({ vote: 'post/Vote' }),
    OnImgLoad() {
      this.loaded += 1
    },
    clickVote(idx) {
      this.vote({
        postId: this.post.id,
        idx: idx === this.post.user_vote ? -1 : idx
      })
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

  transition: all 0.2s;
}

.post-picture:hover {
  background-color: #22c65b;
  border-color: #22c65b;
}
.post-picture.voted {
  background-color: #22c65b;
  border-color: #22c65b;
  transform: scale(1.05);
}
</style>
