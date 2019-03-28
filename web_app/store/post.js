import {
  SuccessNotification,
  ErrorNotification
} from '../helpers/Notifications'

const BaseUrl = 'http://localhost:5000/'

export const state = () => ({
  posts: [],
  votes: [],
  fetchedPosts: false,
  uploading: false
})

export const getters = {
  formated_posts(state, getters, rootState) {
    return state.posts.map(p => {
      const userVote = state.votes.find(
        v => v.user_id === rootState.user.id && v.post_id === p.id
      )
      return { user_vote: userVote !== undefined ? userVote.value : -1, ...p }
    })
  }
}

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
  },
  SET_VOTE(state, { postId, idx, userId }) {
    let res = state.votes.find(
      v => v.user_id === userId && v.post_id === postId
    )
    if (res) {
      res.value = idx
    } else {
      state.votes.push({ user_id: userId, post_id: postId, value: idx })
    }
  }
}

let DebugId = 2
export const actions = {
  async GetPosts({ commit }) {
    try {
      let posts = await this.$axios.$get(BaseUrl + 'post/')
      commit('ADD_POSTS', posts)
      commit('SET_FETCHED_POSTS')
    } catch (error) {
      ErrorNotification(error)
    }
  },
  async Create({ commit }, post) {
    commit('SET_UPLOADING', true)
    const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))
    await sleep(500)
    commit('ADD_POST', { id: DebugId, ...post })
    ++DebugId
    SuccessNotification('Upload successful')
    commit('SET_UPLOADING', false)
  },
  async Vote({ commit, rootState }, { postId, idx }) {
    // commit('SET_UPLOADING', true)
    // const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))
    // await sleep(500)

    commit('SET_VOTE', { postId, idx, userId: rootState.user.id })

    // commit('SET_UPLOADING', false)
  }
}
