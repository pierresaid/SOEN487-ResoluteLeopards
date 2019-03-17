<template>
  <div style="margin-top:50px; display:flex; justify-content:center;">
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
    ...mapState({ posts: state => state.post.posts })
  },
  created() {
    this.$store.dispatch('post/GetPosts')
  }
}
</script>

<style scoped>
</style>
