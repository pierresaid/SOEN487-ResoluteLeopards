<template>
  <div>
    <div class="posts-container">
      <spinner v-if="fetchingPosts"/>
      <Post v-for="(post, index) in posts" :key="index" :post="post"/>
    </div>
  </div>
</template>

<script>
import Post from '~/components/post.vue'
import spinner from '~/components/spinner.vue'
import { mapState } from 'vuex'

export default {
  components: {
    Post,
    spinner
  },
  computed: {
    ...mapState({
      posts: state => state.post.posts,
      fetchingPosts: state => state.post.fetchingPosts
    })
  },
  mounted() {
    if (this.posts.length === 0 && this.fetchingPosts === false) {
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
