<template>
  <div style="width:90%">
    <delimiter/>
    <div style="display:flex; justify-content: space-evenly; align-items: center;">
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

      <!-- <spinner :size="30"/> -->
      <transition name="fade" mode="out-in">
        <spinner v-if="voting !== -1" :size="30"/>
        <span v-else style="width:30px"/>
      </transition>

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
import { mapState, mapActions } from 'vuex'
import spinner from '~/components/spinner.vue'

export default {
  components: {
    delimiter,
    spinner
  },
  props: {
    post: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      voting: -1
    }
  },
  computed: {
    ...mapState({
      isLogged: state => state.user.isLogged
    })
  },
  methods: {
    ...mapActions({ vote: 'post/Vote' }),
    async clickVote(idx) {
      if (this.voting !== -1) return
      if (!this.isLogged) {
        this.launchLoginNotif()
        return
      }

      this.voting = idx
      await this.vote({
        postId: this.post.id,
        value: idx === this.post.user_vote ? -1 : idx
      })
      this.voting = -1
    },
    setVoting(idx) {
      this.voting = idx
    },
    launchLoginNotif() {
      this.$snackbar.open({
        message: 'You must be logged to vote',
        type: 'is-info',
        position: 'is-bottom-right',
        actionText: 'Register',
        onAction: () => {
          this.$nuxt.$router.push({
            path: '/register'
          })
        }
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
