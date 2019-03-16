export const state = () => ({
  name: 'JeanValjean',
  list: []
})

export const mutations = {
  changeName(state, newName) {
    state.name = newName
  },
  remove(state, { todo }) {
    state.list.splice(state.list.indexOf(todo), 1)
  },
  toggle(state, todo) {
    todo.done = !todo.done
  }
}
