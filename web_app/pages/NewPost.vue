<template>
  <no-ssr>
    <div style="margin-top:50px; display: flex; flex-direction:column; align-items: center;">
      <h1 class="title">Create a post</h1>
      <box style="width:50%; max-width:648px;">
        <b-field label="Title" :class="theme">
          <b-input v-model="title" placeholder="Title"/>
        </b-field>
        <p class="label">You Dog Picture</p>
        <span style="margin-bottom:10px;display:flex">
          <c-input
            v-model="url_one"
            placeholder="Dog Picture Url"
            style="width: 100%; margin-right:5px"
            icon="dog"
          />
          <button
            style
            class="control button is-info"
            :class="{'is-loading' : loading_random_dog}"
            :disabled="loading_random_dog"
            @click="getRandomDog"
          >Get random Dog</button>
        </span>
        <div style="display:flex; align-items: center; flex-direction: column;">
          <img
            v-show="img_one_show"
            :src="url_one"
            @load="img_one_err = false; img_one_prediction = null"
            @error="img_one_err = true; img_one_prediction = null"
          >
          <span style="height:10px; margin:25px;">
            <transition enter-active-class="animated fadeInDown" mode="out-in">
              <p v-if="img_one_prediction !== null">{{img_one_prediction}}</p>
              <p
                v-else-if="one_err_message !== null"
                style="color:hsl(348, 100%, 61%)"
              >{{one_err_message}}</p>
            </transition>
          </span>
        </div>
        <p class="label">You Cat Picture</p>
        <span style="margin-bottom:10px;display:flex">
          <c-input
            v-model="url_two"
            placeholder="Cat Picture Url"
            style="width: 100%; margin-right:5px"
            icon="cat"
          />
          <button
            style
            class="control button is-info"
            :class="{'is-loading' : loading_random_cat}"
            :disabled="loading_random_cat"
            @click="getRandomCat"
          >Get random Cat</button>
        </span>
        <div style="display:flex; align-items: center; flex-direction: column">
          <img
            v-show="img_two_show"
            :src="url_two"
            @load="img_two_err = false; img_two_prediction = null"
            @error="img_two_err = true; img_two_prediction = null"
          >
          <span style="height:10px; margin:25px;">
            <transition enter-active-class="animated fadeInDown" mode="out-in">
              <p v-if="img_two_prediction !== null">{{img_two_prediction}}</p>
              <p
                v-else-if="two_err_message !== null"
                style="color:hsl(348, 100%, 61%)"
              >{{two_err_message}}</p>
            </transition>
          </span>
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
import { GetRandomDogUrl, GetRandomCatUrl } from '~/services/imgFetch'
import { ErrorNotification } from '../helpers/Notifications'

import 'animate.css'

export default {
  components: {
    box,
    'c-input': input
  },
  data() {
    return {
      title: 'Hey',
      url_one:
        'https://external-preview.redd.it/ip9lE3gl99wGfqNDP2EF9Y5wpV2DOs8FyKshS42DPsI.jpg?width=640&crop=smart&auto=webp&s=3c8b859244df8c6ba6c864b97a5e06230ed3fdba',
      img_one_err: true,
      img_one_prediction: null,
      url_two:
        'https://preview.redd.it/95sxcsunerp21.jpg?width=640&crop=smart&auto=webp&s=c455765b11111649f583b5d7e140563a641c090d',
      img_two_err: true,
      img_two_prediction: null,
      predict_load: false,
      swap: false,
      one_err_message: null,
      two_err_message: null,
      loading_random_dog: false,
      loading_random_cat: false
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
      let executor_one = () => {}
      this.predict_load = true
      try {
        const res1 = await predictUrl(this.url_one)
        executor_one = () => {
          this.img_one_prediction = `This look like a ${res1}`
          this.one_err_message = null
        }

        try {
          var res2 = await predictUrl(this.url_two)
          this.img_two_prediction = `This look like a ${res2}`
          this.two_err_message = null
          executor_one()
        } catch (error) {
          this.one_err_message = error
          ErrorNotification(error)
        }
      } catch (error) {
        this.two_err_message = error
        ErrorNotification(error)
      }
      if (
        this.img_one_prediction.indexOf('cat') !== -1 &&
        this.img_two_prediction.indexOf('dog') !== -1
      ) {
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
    },
    async getRandomDog() {
      this.loading_random_dog = true
      try {
        const url = await GetRandomDogUrl()
        this.url_one = url
      } catch (error) {
        ErrorNotification(error)
      }
      this.loading_random_dog = false
    },
    async getRandomCat() {
      this.loading_random_cat = true
      try {
        const url = await GetRandomCatUrl()
        this.url_two = url
      } catch (error) {
        ErrorNotification(error)
      }
      this.loading_random_cat = false
    }
  }
}
</script>

<style scoped>
</style>
