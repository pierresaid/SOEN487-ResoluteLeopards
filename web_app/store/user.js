import { Toast } from 'buefy/dist/components/toast'

export const state = () => ({
  id: 1,
  name: 'JeanValjean',
  theme: 'dark',
  uploading: false
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
  }
}

export const actions = {
  async Register({ commit }, user) {
    commit('SET_UPLOADING', true)
    const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))
    await sleep(500)
    console.log(user)

    Toast.open({
      message: 'Welcome !',
      type: 'is-success'
    })
    commit('SET_UPLOADING', false)
  }
}
