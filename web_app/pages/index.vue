<template>
  <div
    v-infinite-scroll="loadMore"
    infinite-scroll-distance="500"
    infinite-scroll-throttle-delay="200"
  >
    <div class="posts-container">
      <Post v-for="(post, index) in posts" :key="index" :post="post"/>
      <spinner v-if="fetchingPosts" style="margin-top:15px; margin-bottom:15px"/>
      <create-more v-if="endOfPosts && !fetchingPosts"/>
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
</style>
