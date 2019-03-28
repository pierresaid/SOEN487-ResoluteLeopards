import {
  SuccessNotification,
  ErrorNotification
} from '../helpers/Notifications'

const BaseUrl = 'http://localhost:5001/'

export const state = () => ({
  isLogged: false,
  id: -1,
  name: null,
  theme: 'dark',
  uploading: false,
  access_token: null,
  refresh_token: null
})

export const mutations = {
  changeName(state, newName) {
    state.name = newName
  },
  toggleTheme(state) {
    state.theme = state.theme === 'light' ? 'dark' : 'light'
  },
  SET_UPLOADING(state, uploading) {
    state.uploading = uploading
  },
  SET_LOGGED(state, logged) {
    state.isLogged = logged
  },
  SET_TOKENS(state, { access_token, refresh_token, id }) {
    this.$axios.defaults.headers.common['Authorization'] = access_token
    state.access_token = access_token
    state.refresh_token = refresh_token
    state.id = id
  },
  SET_INFO(state, { name, mail }) {
    state.name = name
    state.mail = mail
  }
}

export const actions = {
  async Register({ commit }, user) {
    commit('SET_UPLOADING', true)
    try {
      let response = await this.$axios.post(BaseUrl + 'auth/register', {
        name: user.name,
        mail: user.email,
        pwdhash: user.password
      })

      const user_id = response.data.id

      commit('SET_TOKENS', {
        access_token: response.data.access_token,
        refresh_token: response.data.refresh_token,
        id: user_id
      })

      response = await this.$axios.get(BaseUrl + 'users/' + user_id)
      commit('SET_INFO', {
        mail: response.data.mail,
        name: response.data.name
      })
      SuccessNotification('Welcome !')
      commit('SET_UPLOADING', false)
      commit('SET_LOGGED', true)
      return true
    } catch (error) {
      ErrorNotification(error)
    }
    commit('SET_UPLOADING', false)
  },
  async Login({ commit }, user) {
    commit('SET_UPLOADING', true)
    try {
      let response = await this.$axios.post(BaseUrl + 'auth/login', {
        mail: user.email,
        pwdhash: user.password
      })

      const user_id = response.data.id
      commit('SET_TOKENS', {
        access_token: response.data.access_token,
        refresh_token: response.data.refresh_token,
        id: user_id
      })

      response = await this.$axios.get(BaseUrl + 'users/' + user_id)
      commit('SET_INFO', {
        mail: response.data.mail,
        name: response.data.name
      })
      SuccessNotification('Welcome !')
      commit('SET_LOGGED', true)
      commit('SET_UPLOADING', false)
      return true
    } catch (error) {
      ErrorNotification(error)
    }
    commit('SET_UPLOADING', false)
    return false
  },
  async Logout({ commit }) {
    commit('SET_TOKENS', { access_token: null, refresh_token: null, id: -1 })
    commit('SET_LOGGED', false)
  }
}
