export default ({ store, app: { $axios } }) => {
  $axios.defaults.headers.common = {
    Authorization: store.state.user.access_token
  }
}
