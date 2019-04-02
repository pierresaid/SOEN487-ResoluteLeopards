<template>
  <div
    style="margin-top:50px; display:flex; align-items: center; flex-direction:column; justify-content:center;"
  >
    <Post v-for="(post, index) in posts" :key="index" :post="post"/>
  </div>
</template>

<script>
import Post from '~/components/post.vue'
import { mapState } from 'vuex'

export default {
  components: {
    Post
  },
  computed: {
    ...mapState({
      posts: state => state.post.posts
      // postAreFetched: state => state.post.fetchedPosts
    })
  },
  created() {
    if (this.posts.length === 0) this.$store.dispatch('post/GetPosts')
  }
}
</script>

<style scoped>
</style>
