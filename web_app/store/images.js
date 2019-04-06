import { ErrorNotification } from '../helpers/Notifications'

const BaseUrl = 'http://localhost:5003/'

export const state = () => ({
  dogs_urls: [],
  dogs_page: 0,
  cats_urls: [],
  cats_page: 0,
  fetchingDogs: false,
  fetchingCats: false,
  fetchingRandomDog: false,
  fetchingRandomCat: false
})

export const mutations = {
  SET_FETCHING_DOGS(state, status) {
    state.fetchingDogs = status
  },
  SET_FETCHING_RANDOM_DOG(state, status) {
    state.fetchingRandomDog = status
  },
  SET_FETCHING_RANDOM_CAT(state, status) {
    state.fetchingRandomCat = status
  },
  ADD_URLS_DOGS(state, urls) {
    for (let i = 0; i < urls.length; i++) {
      state.dogs_urls.push(urls[i])
    }
    state.dogs_page += 1
  },
  SET_FETCHING_CATS(state, status) {
    state.fetchingCats = status
  },
  ADD_URLS_CATS(state, urls) {
    for (let i = 0; i < urls.length; i++) {
      state.cats_urls.push(urls[i])
    }
    state.cats_page += 1
  }
}

export const actions = {
  async GetDogs({ state, commit }) {
    commit('SET_FETCHING_DOGS', true)
    try {
      let response = await this.$axios.$get(
        BaseUrl + `imgur/dog/${state.dogs_page}`,
        { progress: false }
      )
      commit('ADD_URLS_DOGS', response.images)
    } catch (error) {
      ErrorNotification(error)
    }
    commit('SET_FETCHING_DOGS', false)
  },
  async GetCats({ state, commit }) {
    commit('SET_FETCHING_CATS', true)
    try {
      let response = await this.$axios.$get(
        BaseUrl + `imgur/cat/${state.cats_page}`,
        { progress: false }
      )
      commit('ADD_URLS_CATS', response.images)
    } catch (error) {
      ErrorNotification(error)
    }
    commit('SET_FETCHING_CATS', false)
  },
  async GetRandomCatUrl({ commit }) {
    let res = null
    commit('SET_FETCHING_RANDOM_CAT', true)
    try {
      let response = await this.$axios.$get(`${BaseUrl}cat`)
      res = response.url
    } catch (error) {
      ErrorNotification(error)
    }
    commit('SET_FETCHING_RANDOM_CAT', false)
    return res
  },
  async GetRandomDogUrl({ commit }) {
    let res = null
    commit('SET_FETCHING_RANDOM_DOG', true)
    try {
      let response = await this.$axios.$get(`${BaseUrl}dog`)
      res = response.url
    } catch (error) {
      ErrorNotification(error)
    }
    commit('SET_FETCHING_RANDOM_DOG', false)
    return res
  }
}
