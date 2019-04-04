<template>
  <div>
    <nav
      class="navbar is-fixed-top"
      :class="'is-' + theme"
      style="box-shadow: 0px 0px 5px grey;"
      role="navigation"
      aria-label="main navigation"
    >
      <div class="navbar-brand">
        <nuxt-link to="/" class="navbar-item">
          <img v-if="theme === 'light'" src="~/assets/logo_light.png">
          <img v-else src="~/assets/logo_dark.png">
        </nuxt-link>

        <a
          role="button"
          class="navbar-burger burger"
          :class="{'is-active' : Menuactive}"
          aria-label="menu"
          :aria-expanded="Menuactive"
          data-target="navbarBasicExample"
          @click="Menuactive = !Menuactive"
        >
          <span aria-hidden="true"/>
          <span aria-hidden="true"/>
          <span aria-hidden="true"/>
        </a>
      </div>

      <div
        class="navbar-menu"
        :class="{'is-active' : Menuactive, 'mobile-active-is-dark' : theme === 'dark'}"
      >
        <div class="navbar-start">
          <nuxt-link to="/" class="navbar-item">Home</nuxt-link>
        </div>

        <div style="margin-right:30px" class="navbar-end">
          <div class="navbar-item">
            <nuxt-link to="/NewPost">
              <button class="button is-primary is-info">
                <fa icon="plus" class="fa-lg"/>
              </button>
            </nuxt-link>
          </div>

          <no-ssr>
            <div class="navbar-item">
              <night-mode/>
            </div>

            <div v-if="isLogged" class="navbar-item has-dropdown is-hoverable">
              <a class="navbar-link is-arrowless">
                <avatar style="margin-right:10px" :size="40" :username="userName"/>
                <span>{{userName}}</span>
              </a>

              <div class="navbar-dropdown" :class="{'mobile-active-is-dark' : theme === 'dark'}">
                <nuxt-link to="/Profile">
                  <a style="padding-right:0px" class="navbar-item">Profile</a>
                </nuxt-link>

                <a style="padding-right:0px" class="navbar-item" @click="logout">Logout</a>
              </div>
            </div>

            <div v-else class="navbar-item">
              <div class="buttons">
                <nuxt-link to="/register" class="button is-primary">
                  <strong>Sign up</strong>
                </nuxt-link>
                <nuxt-link to="/login" class="button is-light">Log in</nuxt-link>
              </div>
            </div>
          </no-ssr>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
import NightMode from '~/components/NightMode'
import { mapState, mapActions } from 'vuex'
import Avatar from 'vue-avatar'

export default {
  components: {
    Avatar,
    NightMode
  },
  data() {
    return {
      Menuactive: false
    }
  },
  computed: {
    ...mapState({
      userName: state => state.user.name,
      theme: state => state.user.theme,
      isLogged: state => state.user.isLogged
    })
  },
  methods: {
    ...mapActions({ logout: 'user/Logout' })
  }
}
</script>
