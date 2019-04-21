export default ({ store, app: { $axios } }) => {
  $axios.defaults.headers.common = {
    Authorization: `Bearer ${store.state.user.access_token}`
  }
}
