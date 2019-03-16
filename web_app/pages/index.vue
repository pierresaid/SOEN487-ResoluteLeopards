<template>
  <div style="margin-top:50px">
    <Post v-for="(post, index) in posts" :key="index" :post="post"/>
    <fa icon="thumbs-up"/>
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
  async fetch({ store }) {
    await store.dispatch('post/GET_POSTS')
  }
}
</script>

<style scoped>
</style>
