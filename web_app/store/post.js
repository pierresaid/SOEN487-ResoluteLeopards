import { Toast } from 'buefy/dist/components/toast'

export const state = () => ({
  posts: [],
  fetchedPosts: false,
  uploading: false
})

export const mutations = {
  SET_FETCHED_POSTS(state) {
    state.fetchedPosts = true
  },
  SET_POSTS(state, posts) {
    state.posts = posts
  },
  ADD_POST(state, post) {
    state.posts.push(post)
  },
  ADD_POSTS(state, posts) {
    state.posts = state.posts.concat(posts)
  },
  SET_UPLOADING(state, uploading) {
    state.uploading = uploading
  }
}

let DebugId = 2
export const actions = {
  async GetPosts({ commit }) {
    try {
      let posts = await this.$axios.$get('post/')
      commit('ADD_POSTS', posts)
      commit('SET_FETCHED_POSTS')
    } catch (error) {
      Toast.open({
        message: error,
        type: 'is-danger'
      })
    }
  },
  async Create({ commit }, post) {
    commit('SET_UPLOADING', true)
    const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))
    await sleep(500)
    commit('ADD_POST', { id: DebugId, ...post })
    ++DebugId
    Toast.open({
      message: 'Upload successful',
      type: 'is-success'
    })
    commit('SET_UPLOADING', false)
  }
}
