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
  POP_POST(state, postId) {
    const idx = state.posts.findIndex(p => {
      return p.id === postId
    })
    state.posts.splice(idx, 1)
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
    console.log(post)

    state.posts[idx].user_vote = post.user_vote
    state.posts[idx].vote_one = post.vote_one
    state.posts[idx].vote_two = post.vote_two
  },
  SET_END(state, value) {
    state.end = value
  }
}

export const actions = {
  async GetPosts({ state, commit, rootState }) {
    try {
      commit('SET_FETCHING_POSTS', true)
      let response = await this.$axios.$get(BaseUrl + 'post', {
        params: {
          page: state.page,
          post_per_page: state.post_per_page,
          user_id: rootState.user.id
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
          return { ...p, author_name: gen_name() }
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

  async removePost({ commit }, postId) {
    commit('POP_POST', postId)
    SuccessNotification('Update successful')

    // commit('SET_UPLOADING', true)
    // try {
    //   let response = await this.$axios.post(BaseUrl + 'post', {
    //     title: post.title,
    //     url_one: post.url_one,
    //     url_two: post.url_two,
    //     user_id: rootState.user.id
    //   })
    //   commit('ADD_POST', response.data.post)
    // SuccessNotification('Upload successful')
    // } catch (error) {
    //   ErrorNotification(error)
    // }
    // commit('SET_UPLOADING', false)
  },
  async Vote({ commit, rootState }, { postId, value }) {
    // commit('SET_UPLOADING_VOTE', true)
    try {
      let response = await this.$axios.post(BaseUrl + 'vote/', {
        post_id: postId,
        user_id: rootState.user.id,
        value: value
      })

      response = await this.$axios.get(BaseUrl + `post/${postId}`, {
        params: {
          user_id: rootState.user.id
        }
      })
      commit('SET_POST', response.data.post)
    } catch (error) {
      ErrorNotification(error)
    }

    // commit('SET_UPLOADING_VOTE', false)
  }
}
