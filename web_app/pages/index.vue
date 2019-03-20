<template>
  <div
    style="margin-top:50px; display:flex; align-items: center; flex-direction:column; justify-content:center;"
  >
    <Post v-for="(post, index) in posts" :key="index" :post="post"/>
  </div>
</template>

<script>
import Post from '~/components/post.vue'
import { mapState, mapGetters } from 'vuex'

export default {
  components: {
    Post
  },
  computed: {
    ...mapState({
      postAreFetched: state => state.post.fetchedPosts
    }),
    ...mapGetters({ posts: 'post/formated_posts' })
  },
  created() {
    if (!this.postAreFetched) this.$store.dispatch('post/GetPosts')
  }
}
</script>

<style scoped>
</style>
