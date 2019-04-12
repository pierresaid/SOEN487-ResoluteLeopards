<template>
  <div style="width:90%">
    <delimiter/>
    <div style="display:flex; justify-content: space-around;">
      <div style="display:flex; align-items:center">
        <transition :duration="100" name="fade-long" mode="out-in">
          <fa
            v-if="post.user_vote == 0"
            key="2"
            class="heart"
            :icon="['fas', 'heart']"
            @click="clickVote(0)"
          />
          <fa v-else key="1" class="heart" :icon="['far', 'heart']" @click="clickVote(0)"/>
        </transition>
        <p>{{post.vote_one}} votes</p>
      </div>
      <div style="display:flex; align-items:center">
        <transition :duration="100" name="fade-long" mode="out-in">
          <fa
            v-if="post.user_vote == 1"
            key="2"
            class="heart"
            :icon="['fas', 'heart']"
            @click="clickVote(1)"
          />
          <fa v-else key="1" class="heart" :icon="['far', 'heart']" @click="clickVote(1)"/>
        </transition>
        <p>{{post.vote_two}} votes</p>
      </div>
    </div>
  </div>
</template>

<script>
import delimiter from './delimiter'
import { mapActions } from 'vuex'

export default {
  components: {
    delimiter
  },
  props: {
    post: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {}
  },
  methods: {
    ...mapActions({ vote: 'post/Vote' }),
    clickVote(idx) {
      this.vote({
        postId: this.post.id,
        value: idx === this.post.user_vote ? -1 : idx
      })
    }
  }
}
</script>

<style scoped>
.fade-long-enter-active,
.fade-long-leave-active {
  transition: opacity 0.5s;
}
.fade-long-enter,
.fade-long-leave-to {
  opacity: 0;
}

.heart {
  color: #ff007e;
  width: 50px;
  height: 50px;
  margin: 10px;
  user-select: none;
  -moz-user-select: none;
  -webkit-user-drag: none;
  -webkit-user-select: none;
  -ms-user-select: none;
  cursor: pointer;
}
</style>
