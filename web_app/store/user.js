export const state = () => ({
  name: 'JeanValjean',
  theme: 'dark'
})

export const mutations = {
  changeName(state, newName) {
    state.name = newName
  },
  toggleTheme(state) {
    state.theme = state.theme === 'light' ? 'dark' : 'light'
  }
}
