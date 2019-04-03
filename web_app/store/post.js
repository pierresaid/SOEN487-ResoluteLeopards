import {
  SuccessNotification,
  ErrorNotification
} from '../helpers/Notifications'

const BaseUrl = 'http://localhost:5000/'

export const state = () => ({
  posts: [],
  // votes: [],
  fetchedPosts: false,
  uploading: false,
  page: 1,
  post_per_page: 10
})

export const mutations = {
  SET_FETCHING_POSTS(state, status) {
    state.fetchedPosts = status
  },
  SET_POSTS(state, posts) {
    state.posts = posts
  },
  ADD_POST(state, post) {
    state.posts.push(post)
  },
  ADD_POSTS(state, posts) {
    console.log('posts : ', posts)

    for (let i = 0; i < posts.length; i++) {
      state.posts.push(posts[i])
    }
    state.page += 1
  },
  SET_UPLOADING(state, uploading) {
    state.uploading = uploading
  },
  SET_VOTE(state, { postId, idx, userId }) {
    let res = state.posts.find(p => p.id === postId)
    if (res) {
      res.user_vote = idx
    }
  }
}

export const actions = {
  async GetPosts({ state, commit }) {
    try {
      commit('SET_FETCHING_POSTS', true)
      let response = await this.$axios.$get(BaseUrl + 'post/', {
        params: {
          // page: state.page,
          // post_per_page: state.post_per_page
        }
      })
      commit('ADD_POSTS', response.posts)
      commit('SET_FETCHING_POSTS', false)
    } catch (error) {
      console.log(error)

      ErrorNotification(error)
    }
  },
  async Create({ commit }, post) {
    commit('SET_UPLOADING', true)
    try {
      let response = await this.$axios.post(BaseUrl + 'post/', {
        title: post.title,
        url_one: post.url_one,
        url_two: post.url_two
      })
      commit('ADD_POST', response.data.post)
      SuccessNotification('Upload successful')
    } catch (error) {
      ErrorNotification(error)
    }

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
