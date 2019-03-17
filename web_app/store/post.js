import { Toast } from 'buefy/dist/components/toast'

export const state = () => ({
  posts: []
})

export const mutations = {
  SET_POSTS(state, posts) {
    state.posts = posts
  }
}

export const actions = {
  async GetPosts({ commit }) {
    try {
      let posts = await this.$axios.$get('post/')
      commit('SET_POSTS', posts)
    } catch (error) {
      Toast.open({
        message: error,
        type: 'is-danger'
      })
    }
  }
}
