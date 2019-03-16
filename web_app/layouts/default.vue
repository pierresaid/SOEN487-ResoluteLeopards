<template>
  <div>
    <nav class="navbar is-fixed-top" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <nuxt-link to="/" class="navbar-item">
          <img src="~/assets/logo.png">
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

      <div id="navbarBasicExample" class="navbar-menu" :class="{'is-active' : Menuactive}">
        <div class="navbar-start">
          <nuxt-link to="/" class="navbar-item">Home</nuxt-link>
          <nuxt-link to="/user" class="navbar-item">Users</nuxt-link>
        </div>

        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <a class="button is-primary">
                <strong>Sign up</strong>
              </a>
              <a class="button is-light">Log in</a>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <section class="section">
      <div class="container">
        <nuxt/>
      </div>
    </section>

    <footer class="footer">
      <div class="content has-text-centered">
        <p>
          <strong>Cat vs Dog</strong> by the ResoluteLeopards for the SOEN487 Project
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      Menuactive: false
    }
  }
}
</script>

<style scoped>
.container {
  /* margin: 0 auto; */
  min-height: 100vh;
  /* display: flex; */
  /* justify-content: center; */
  /* align-items: center; */
  /* text-align: center; */
}
</style>
