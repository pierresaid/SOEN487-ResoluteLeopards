import {
  // SuccessNotification,
  ErrorNotification
} from '../helpers/Notifications'

const BaseUrl = 'http://localhost:5004/'

export const state = () => ({
  cats: -1,
  dogs: -1,
  loading: false
})

export const mutations = {
  SET_LOADING(state, status) {
    state.loading = status
  },
  SET_INFO(state, { cats, dogs }) {
    state.cats = 25
    // state.cats = cats
    // state.dogs = dogs
    state.dogs = 42
  }
}

export const actions = {
  async getResults({ commit }, user) {
    commit('SET_LOADING', true)
    try {
      let response = await this.$axios.get(BaseUrl + 'results')

      commit('SET_INFO', {
        cats: response.data.cats,
        dogs: response.data.dogs
      })

      commit('SET_LOADING', false)
    } catch (error) {
      ErrorNotification(error)
    }
    commit('SET_LOADING', false)
  }
}
