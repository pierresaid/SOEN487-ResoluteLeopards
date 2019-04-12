<template>
  <div
    v-infinite-scroll="loadMore"
    infinite-scroll-distance="500"
    infinite-scroll-throttle-delay="200"
  >
    <div class="posts-container">
      <transition-group
        name="list-animated"
        style="display:flex; flex-direction:column; align-items:center"
      >
        <Post v-for="post in posts" :key="post.id" class="list-animated-item" :post="post"/>
        <create-more
          v-if="endOfPosts && !fetchingPosts"
          key="create-more"
          style="width: fit-content"
          class="list-animated-item"
        />
      </transition-group>
      <spinner v-if="fetchingPosts" style="margin-top:15px; margin-bottom:15px"/>
    </div>
  </div>
</template>

<script>
import Post from '~/components/post.vue'
import spinner from '~/components/spinner.vue'
import createMore from '~/components/createMore.vue'
import { mapState } from 'vuex'

export default {
  components: {
    Post,
    spinner,
    createMore
  },
  computed: {
    ...mapState({
      posts: state => state.post.posts,
      fetchingPosts: state => state.post.fetchingPosts,
      endOfPosts: state => state.post.end
    }),
    disableLoading() {
      return this.fetchingPosts || this.endOfPosts
    }
  },
  methods: {
    loadMore() {
      if (this.disableLoading) return
      this.$store.dispatch('post/GetPosts')
    }
  }
}
</script>

<style scoped>
.posts-container {
  margin-top: 50px;
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
}

.list-animated-item {
  transition: opacity 1s, transform 1s;
  margin-right: 10px;
}
.list-animated-enter,
.list-animated-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
.list-animated-leave-active {
  position: absolute;
}
</style>
