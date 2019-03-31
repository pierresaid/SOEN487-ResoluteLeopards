<template>
  <no-ssr>
    <div style="margin-top:50px; display: flex; flex-direction:column; align-items: center;">
      <h1 class="title">Create a post</h1>
      <box style="width:50%; max-width:648px;">
        <b-field label="Title" :class="theme">
          <b-input v-model="title" placeholder="Title"/>
        </b-field>
        <b-field label="Your Dog Picture" style="width:100%;" :class="theme">
          <c-input v-model="url_one" placeholder="Dog Picture Url" style="width: 100%;" icon="dog"/>
        </b-field>
        <div style="display:flex; align-items: center;">
          <img
            v-show="img_one_show"
            :src="url_one"
            @load="img_one_err = false"
            @error="img_one_err = true"
          >
          <p v-show="img_one_prediction !== null" style="margin-left:25px;">{{img_one_prediction}}</p>
        </div>
        <b-field label="Your Cat Picture" style="width:100%;" :class="theme">
          <c-input v-model="url_two" placeholder="Cat Picture Url" style="width: 100%;" icon="cat"/>
        </b-field>
        <div style="display:flex; align-items: center;">
          <img
            v-show="img_two_show"
            :src="url_two"
            @load="img_two_err = false"
            @error="img_two_err = true"
          >
          <p v-show="img_two_prediction !== null" style="margin-left:25px;">{{img_two_prediction}}</p>
        </div>
        <b-field style="margin-top:10px; width:100%;" class="is-grouped" :class="theme">
          <button
            :disabled="FormHasError"
            class="control button is-success"
            :class="{'is-loading' : uploading}"
            @click="create(new_post)"
          >Submit</button>
          <button
            class="control button is-info"
            :class="{'is-loading' : predict_load}"
            :disabled="!img_one_show || !img_two_show || predict_load"
            @click="predictImages"
          >
            <fa icon="robot" style="margin-right:5px"/>Predict
          </button>
          <button v-if="swap" class="control button is-info" @click="swapImages">
            <fa icon="sync-alt" style="margin-right:5px"/>Swap
          </button>
        </b-field>
      </box>
    </div>
  </no-ssr>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import box from '~/components/box'
import input from '~/components/input'
import predictUrl from '~/services/prediction'

export default {
  components: {
    box,
    'c-input': input
  },
  data() {
    return {
      title: '',
      url_one: null,
      img_one_err: true,
      img_one_prediction: null,
      url_two: null,
      img_two_err: true,
      img_two_prediction: null,
      predict_load: false,
      swap: false
    }
  },
  computed: {
    ...mapState({
      theme: state => state.user.theme,
      uploading: state => state.post.uploading
    }),
    new_post() {
      return {
        title: this.title,
        url_one: this.url_one,
        url_two: this.url_two
      }
    },
    FormHasError() {
      return (
        this.img_one_err ||
        this.img_two_err ||
        this.title === '' ||
        this.url_one === null ||
        this.url_two === null
      )
    },
    img_one_show() {
      return !this.img_one_err && this.url_one !== null
    },
    img_two_show() {
      return !this.img_two_err && this.url_two !== null
    }
  },
  methods: {
    ...mapActions({ create: 'post/Create' }),
    async predictImages() {
      this.predict_load = true
      const res1 = await predictUrl(this.url_one)
      const res2 = await predictUrl(this.url_two)
      this.img_one_prediction = `This look like a ${res1}`
      this.img_two_prediction = `This look like a ${res2}`
      if (res1 === 'cat' && res2 === 'dog') {
        this.swap = true
      }
      this.predict_load = false
    },
    swapImages() {
      let tmp = this.url_one
      this.url_one = this.url_two
      this.url_two = tmp
      tmp = this.img_one_prediction
      this.img_one_prediction = this.img_two_prediction
      this.img_two_prediction = tmp
      this.swap = false
    }
  }
}
</script>

<style scoped>
</style>
