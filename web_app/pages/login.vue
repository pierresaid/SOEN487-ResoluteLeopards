<template>
  <no-ssr>
    <div style="margin-top:50px; display: flex; flex-direction:column; align-items: center;">
      <h1 class="title">Login</h1>
      <box style="width:50%; max-width:648px;">
        <b-field label="Email" :class="theme">
          <c-input v-model="email" type="email" placeholder="Email" icon="envelope"/>
        </b-field>

        <b-field label="Password" style="width:100%;" :class="theme">
          <c-input v-model="password" type="password" placeholder="Password" icon="lock"/>
        </b-field>

        <button
          :disabled="FormHasError"
          style="margin-top:10px"
          class="button is-success"
          :class="{'is-loading' : uploading}"
          @click="submit"
        >Submit</button>
      </box>
    </div>
  </no-ssr>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import box from '~/components/box'
import input from '~/components/input'

export default {
  components: {
    box,
    'c-input': input
  },
  data() {
    return {
      email: '',
      password: '',
      emailError: false
    }
  },
  computed: {
    ...mapState({
      theme: state => state.user.theme,
      uploading: state => state.user.uploading
    }),
    FormHasError() {
      const validateEmail = email => {
        var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        return re.test(email)
      }
      return (
        this.email === '' || this.password === '' || !validateEmail(this.email)
      )
    }
  },
  methods: {
    ...mapActions({ login: 'user/Login' }),
    async submit() {
      let res = await this.login({ email: this.email, password: this.password })
      if (res) this.$nuxt.$router.replace({ path: '/' })
    }
  }
}
</script>

<style scoped>
</style>
