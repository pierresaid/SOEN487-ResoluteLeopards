<template>
  <div v-show="loaded === 2" class="box post" :class="theme">
    <div style="display:flex; width:100%; justify-content:space-between">
      <div style="width:36px"/>
      <h1 style="margin-bottom: 10px" class="title">{{post.title}}</h1>

      <b-dropdown v-if="post.author_id == user_id" aria-role="list">
        <button
          slot="trigger"
          class="button"
          style="background-color:transparent; border-color:transparent"
        >
          <fa class="icon" icon="ellipsis-v"/>
        </button>

        <b-dropdown-item aria-role="listitem" @click="$nextTick(() => { removePost(post.id)})">
          <fa icon="trash" style="margin-right:10px; color:red"/>Remove
        </b-dropdown-item>
      </b-dropdown>

      <span v-else style="width:36px"/>
    </div>
    <h2 style="color:#adadad" class="subtitle">{{post.author_name}}</h2>
    <div style="display:flex; flex-wrap: wrap; justify-content:center; align-items: center;">
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
    <post-votes ref="voteComp" :post="post"/>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import PostVotes from './PostVotes'
export default {
  components: {
    PostVotes
  },
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
    ...mapState({
      theme: state => state.user.theme,
      user_id: state => state.user.id
    })
  },
  methods: {
    ...mapActions({ vote: 'post/Vote', removePost: 'post/removePost' }),
    OnImgLoad() {
      this.loaded += 1
    },
    async clickVote(idx) {
      if (this.$refs.voteComp.voting !== -1) return
      this.$refs.voteComp.setVoting(idx)
      await this.vote({
        postId: this.post.id,
        value: idx === this.post.user_vote ? -1 : idx
      })
      this.$refs.voteComp.setVoting(-1)
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
  margin: 10px;
  max-height: 50%;
  max-width: 48%;
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

.animated {
  -webkit-animation-duration: 0.5s;
  animation-duration: 0.5s;
  -webkit-animation-fill-mode: both;
  animation-fill-mode: both;
}

.dropdown-item {
  color: black;
}
</style>
