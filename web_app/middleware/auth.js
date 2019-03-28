export default function({ store, redirect }) {
  if (!store.state.user.isLogged) {
    return redirect('/login')
  }
}
