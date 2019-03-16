import axios from 'axios'

export const state = () => ({
  posts: [{ title: 'azd' }]
})

export const mutations = {
  SetPosts(state, posts) {
    state.posts = posts
  }
}

export const actions = {
  async GET_POSTS(context) {
    let { data } = await axios.get('http://127.0.0.1:5000/post/')
    context.commit('SetPosts', data)
  }
}
