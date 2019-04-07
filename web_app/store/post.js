import {
  SuccessNotification,
  ErrorNotification
} from '../helpers/Notifications'

import Vue from 'vue'

const BaseUrl = 'http://localhost:5000/'

export const state = () => ({
  posts: [],
  fetchingPosts: false,
  uploading: false,
  page: 0,
  post_per_page: 10,
  end: false
})

export const mutations = {
  SET_FETCHING_POSTS(state, status) {
    state.fetchingPosts = status
  },
  SET_POSTS(state, posts) {
    state.posts = posts
  },
  ADD_POST(state, post) {
    state.posts.push(post)
  },
  ADD_POSTS(state, posts) {
    for (let i = 0; i < posts.length; i++) {
      state.posts.push(posts[i])
    }
    state.page += 1
  },
  SET_UPLOADING(state, uploading) {
    state.uploading = uploading
  },
  SET_POST(state, post) {
    let idx = state.posts.findIndex(p => {
      return p.id === post.id
    })
    Vue.set(state.posts, idx, post)
  },
  SET_END(state, value) {
    state.end = value
  }
}

export const actions = {
  async GetPosts({ state, commit }) {
    try {
      commit('SET_FETCHING_POSTS', true)
      let response = await this.$axios.$get(BaseUrl + 'post', {
        params: {
          page: state.page,
          post_per_page: state.post_per_page
        },
        progress: false
      })

      if (response.end === true) {
        commit('SET_END', true)
      } else {
        // DEBUG
        const gen_name = () => {
          const names = [
            'Jean-Valjean',
            'Jean-Philippe',
            'Jean-Jean',
            'Jean-Clement',
            'Jean-Théo',
            'Jean-Mohamed'
          ]
          return names[Math.floor((Math.random() * 100) % names.length)]
        }
        response.posts = response.posts.map(p => {
          return { ...p, user_vote: -1, author_name: gen_name() }
        })
        commit('ADD_POSTS', response.posts)
      }
      commit('SET_FETCHING_POSTS', false)
    } catch (error) {
      ErrorNotification(error)
    }
  },
  async Create({ commit, rootState }, post) {
    commit('SET_UPLOADING', true)
    try {
      let response = await this.$axios.post(BaseUrl + 'post', {
        title: post.title,
        url_one: post.url_one,
        url_two: post.url_two,
        user_id: rootState.user.id
      })
      commit('ADD_POST', response.data.post)
      SuccessNotification('Upload successful')
    } catch (error) {
      ErrorNotification(error)
    }
    commit('SET_UPLOADING', false)
  },
  async Vote({ commit, state }, { postId, value }) {
    // commit('SET_UPLOADING_VOTE', true)
    try {
      // const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))
      // await sleep(500)

      // let response = await this.$axios.put(BaseUrl + 'post ', {
      //   title: post.title,
      //   url_one: post.url_one,
      //   url_two: post.url_two,
      //   user_id: rootState.user.id
      // })
      let post = state.posts.find(p => {
        return p.id == postId
      })
      let ze_post = { ...post }
      let new_one = ze_post.vote_one
      let new_two = ze_post.vote_two
      if (ze_post.user_vote === 0 && value === 1) {
        new_one -= 1
        new_two += 1
      } else if (ze_post.user_vote === 1 && value === 0) {
        new_one += 1
        new_two -= 1
      } else {
        new_one +=
          value === 0 ? 1 : value === -1 && ze_post.user_vote === 0 ? -1 : 0
        new_two +=
          value === 1 ? 1 : value === -1 && ze_post.user_vote === 1 ? -1 : 0
      }
      ze_post.user_vote = value
      ze_post.vote_one = new_one
      ze_post.vote_two = new_two

      commit('SET_POST', ze_post)
    } catch (error) {
      ErrorNotification(error)
    }

    // commit('SET_UPLOADING_VOTE', false)
  }
}
