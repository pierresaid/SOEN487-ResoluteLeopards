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
          <img v-if="theme === 'light'" src="~/assets/logo-light.png">
          <img v-else src="~/assets/logo-dark.png">
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

      <div class="navbar-menu" :class="{'is-active' : Menuactive}">
        <div class="navbar-start">
          <nuxt-link to="/" class="navbar-item">Home</nuxt-link>
        </div>

        <div class="navbar-end">
          <div class="navbar-item">
            <nuxt-link to="/NewPost">
              <button class="button is-primary is-info">
                <fa icon="plus" class="fa-lg"/>
              </button>
            </nuxt-link>
          </div>

          <div class="navbar-item">
            <night-mode/>
          </div>
          <div class="navbar-item">
            <div class="buttons">
              <button class="button is-primary">
                <strong>Sign up</strong>
              </button>
              <button class="button is-light">Log in</button>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <section class="section" :class="theme === 'light' ? 'background' : 'dark-background'">
      <div class="container">
        <nuxt :class="'app-is-' + theme"/>
      </div>
    </section>

    <footer class="footer" :class="theme">
      <div class="content has-text-centered">
        <p>
          <strong>Cat vs Dog</strong> by the ResoluteLeopards for the SOEN487 Project
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
import NightMode from '~/components/NightMode'
import { mapState } from 'vuex'

export default {
  components: {
    NightMode
  },
  data() {
    return {
      Menuactive: false
    }
  },
  head() {
    return {
      titleTemplate: 'Cat VS Dog',
      meta: [
        {
          content: 'The only battle worth fighting'
        }
      ]
    }
  },
  computed: {
    ...mapState({ theme: state => state.user.theme })
  }
}
</script>

<style>
.container {
  min-height: 100vh;
}
.dark {
  background-color: rgb(26, 26, 27);
}
.app-is-dark :not(input) {
  color: white;
}

.dark :not(input) {
  color: white;
}

.background {
  background-color: #dae0e6;
}

.dark-background {
  background-color: black;
}
</style>
