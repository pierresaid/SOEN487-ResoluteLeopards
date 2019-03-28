<template>
  <div style="margin-top:50px; display: flex; flex-direction:column; align-items: center;">
    <h1 class="title">Profile</h1>
    <box
      class="l-size"
      style="min-width:20%; display:flex; flex-direction:column; align-items: center;"
    >
      <div>
        <div>
          <div style="display:flex; align-items:center">
            <fa icon="user"/>
            <h3 style="margin-left:15px" class="label">Name</h3>
          </div>
          <p>{{name}}</p>
        </div>
        <div>
          <div style="display:flex; align-items:center">
            <fa icon="envelope"/>
            <h3 style="margin-left:15px" class="label">Mail</h3>
          </div>
          <p>{{mail}}</p>
        </div>
      </div>
    </box>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import box from '~/components/box'

export default {
  middleware: 'auth',
  components: {
    box
  },
  computed: {
    ...mapState({
      name: state => state.user.name,
      mail: state => state.user.mail
    })
  }
}
</script>

<style scoped>
</style>
