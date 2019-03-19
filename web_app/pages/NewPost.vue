<template>
  <div style="margin-top:50px; display: flex; flex-direction:column; align-items: center;">
    <h1 class="title">Create a post</h1>
    <box style="width:50%; max-width:648px;">
      <b-field label="Title" :class="theme">
        <b-input v-model="title" placeholder="Title"/>
      </b-field>
      <b-field label="Your Dog Picture" style="width:100%;" :class="theme">
        <div style="display:flex; align-items: center;">
          <fa icon="dog" style="margin-right:10px"/>
          <b-input v-model="url_one" placeholder="Dog Picture Url" style="width: 100%;"/>
        </div>
      </b-field>
      <img
        v-show="!img_one_err && url_one !== null"
        :src="url_one"
        @load="img_one_err = false"
        @error="img_one_err = true"
      >

      <b-field label="Your Cat Picture" style="width:100%;" :class="theme">
        <div style="display:flex; align-items: center;">
          <fa icon="cat" style="margin-right:10px"/>
          <b-input v-model="url_two" placeholder="Cat Picture Url" style="width: 100%;"/>
        </div>
      </b-field>
      <img
        v-show="!img_two_err && url_two !== null"
        :src="url_two"
        @load="img_two_err = false"
        @error="img_two_err = true"
      >
      <button
        :disabled="FormHasError"
        style="margin-top:10px"
        class="button is-success"
        @click="create(new_post)"
      >Submit</button>
    </box>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import box from '~/components/box'

export default {
  components: {
    box
  },
  data() {
    return {
      title: '',
      url_one: null,
      img_one_err: false,
      url_two: null,
      img_two_err: false
    }
  },
  computed: {
    ...mapState({ theme: state => state.user.theme }),
    new_post() {
      return {
        title: this.title,
        url_one: this.url_one,
        url_two: this.url_two
      }
    },
    FormHasError() {
      return (
        false &&
        (this.img_one_err ||
          this.img_two_err ||
          this.title === '' ||
          this.url_one === null ||
          this.url_two === null)
      )
    }
  },
  methods: {
    ...mapActions({ create: 'post/Create' })
  }
}
</script>

<style scoped>
</style>
