<template>
  <no-ssr>
    <div style="margin-top:50px; display: flex; flex-direction:column; align-items: center;">
      <h1 class="title">Create a post</h1>
      <box style="width:80%; max-width:800px;">
        <b-field label="Title" :class="theme">
          <b-input v-model="title" placeholder="Title"/>
        </b-field>
        <p class="label">You Dog Picture</p>
        <b-field style="margin-bottom:10px;display:flex" :type="{'is-danger' : img_one_err}">
          <c-input
            v-model="url_one"
            placeholder="Dog Picture Url"
            style="width: 100%; margin-right:5px"
            icon="dog"
          />
          <div class="field has-addons">
            <p class="control">
              <button
                class="control button is-info"
                :class="{'is-loading' : loading_random_dog}"
                :disabled="loading_random_dog"
                @click="getRandomDog"
              >Get random Dog</button>
            </p>
            <p class="control">
              <imgur-browser
                v-model="url_one"
                :images="DogImages"
                :fetch-more-images="fetchMoreDogs"
                :fetching="fetchingDogs"
                title="Chose a dog"
              />
            </p>
          </div>
        </b-field>

        <div style="display:flex; align-items: center; flex-direction: column;">
          <on-top>
            <img
              v-show="img_one_show"
              slot="parent"
              class="chosen-image"
              :src="url_one"
              @load="img_one_err = false; img_one_prediction = null; loading_img_one = false; loaded_once_one = true"
              @error="img_one_err = true; img_one_prediction = null; loading_img_one = false; loaded_once_one = true"
            >
            <spinner v-show="loading_img_one && img_one_show" slot="child" background/>
          </on-top>
          <spinner v-show="loading_img_one && !img_one_show" style="margin-top:20px;"/>

          <span style="height:10px; margin:25px;">
            <transition enter-active-class="animated fadeInDown" mode="out-in">
              <p v-if="img_one_prediction !== null">
                I am
                <b>{{img_one_prediction.percentage}}</b>
                sure that this is a
                <b>{{img_one_prediction.label}}</b>
              </p>
              <p
                v-else-if="one_err_message !== null"
                style="color:hsl(348, 100%, 61%)"
              >{{one_err_message}}</p>
            </transition>
          </span>
        </div>
        <p class="label">You Cat Picture</p>
        <b-field style="margin-bottom:10px;display:flex" :type="{'is-danger' : img_two_err}">
          <c-input
            v-model="url_two"
            placeholder="Cat Picture Url"
            style="width: 100%; margin-right:5px"
            icon="cat"
          />

          <div class="field has-addons">
            <p class="control">
              <button
                class="control button is-info"
                :class="{'is-loading' : loading_random_cat}"
                :disabled="loading_random_cat"
                @click="getRandomCat"
              >Get random Cat</button>
            </p>
            <p class="control">
              <imgur-browser
                v-model="url_two"
                :images="CatImages"
                :fetch-more-images="fetchMoreCats"
                :fetching="fetchingCats"
                title="Chose a cat"
              />
            </p>
          </div>
        </b-field>
        <div style="display:flex; align-items: center; flex-direction: column">
          <on-top>
            <img
              v-show="img_two_show"
              slot="parent"
              class="chosen-image"
              :src="url_two"
              @load="img_two_err = false; img_two_prediction = null; loading_img_two = false; loaded_once_two = true;"
              @error="img_two_err = true; img_two_prediction = null; loading_img_two = false; loaded_once_two = true;"
            >
            <spinner v-show="loading_img_two && img_two_show" slot="child" background/>
          </on-top>
          <spinner v-show="loading_img_two && !img_two_show" style="margin-top:20px;"/>

          <span style="height:10px; margin:25px;">
            <transition enter-active-class="animated fadeInDown" mode="out-in">
              <p v-if="img_two_prediction !== null">
                I am
                <b>{{img_two_prediction.percentage}}</b>
                % sure that this is a
                <b>{{img_two_prediction.label}}</b>
              </p>
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
import onTop from '~/components/onTop'
import predictUrl from '~/services/prediction'
import { ErrorNotification } from '../helpers/Notifications'
import spinner from '~/components/spinner.vue'

import 'animate.css'
import ImgurBrowser from '../components/ImgurBrowser.vue'

export default {
  components: {
    box,
    spinner,
    'c-input': input,
    onTop,
    ImgurBrowser
  },
  middleware: 'auth',
  data() {
    return {
      title: '',
      url_one: null,
      img_one_err: false,
      img_one_prediction: null,
      url_two: null,
      img_two_err: false,
      img_two_prediction: null,
      predict_load: false,
      one_err_message: null,
      two_err_message: null,
      loading_img_one: false,
      loading_img_two: false,
      loaded_once_one: false,
      loaded_once_two: false
    }
  },
  computed: {
    ...mapState({
      theme: state => state.user.theme,
      uploading: state => state.post.uploading,
      CatImages: state => state.images.cats_urls,
      DogImages: state => state.images.dogs_urls,
      fetchingDogs: state => state.images.fetchingDogs,
      fetchingCats: state => state.images.fetchingCats,
      loading_random_dog: state => state.images.fetchingRandomDog,
      loading_random_cat: state => state.images.fetchingRandomCat
    }),
    new_post() {
      return {
        title: this.title,
        url_one: this.url_one,
        url_two: this.url_two
      }
    },
    swap() {
      return (
        this.img_one_prediction !== null &&
        this.img_one_prediction.label.indexOf('cat') !== -1 &&
        this.img_two_prediction !== null &&
        this.img_two_prediction.label.indexOf('dog') !== -1
      )
    },
    FormHasError() {
      return (
        this.img_one_err ||
        this.img_two_err ||
        this.title === '' ||
        this.url_one === null ||
        this.url_two === null ||
        !this.loaded_once_one ||
        !this.loaded_once_two
      )
    },
    img_one_show() {
      return !this.img_one_err && this.url_one !== null && this.loaded_once_one
    },
    img_two_show() {
      return !this.img_two_err && this.url_two !== null && this.loaded_once_two
    }
  },
  watch: {
    url_one(newValue, oldValue) {
      this.loading_img_one = true
    },
    url_two(newValue, oldValue) {
      this.loading_img_two = true
    }
  },
  methods: {
    ...mapActions({
      create: 'post/Create',
      fetchMoreDogs: 'images/GetDogs',
      fetchMoreCats: 'images/GetCats',
      GetRandomCatUrl: 'images/GetRandomCatUrl',
      GetRandomDogUrl: 'images/GetRandomDogUrl'
    }),

    async predictImages() {
      let executor_one = () => {}
      this.predict_load = true
      try {
        const res1 = await predictUrl(this.url_one)
        executor_one = () => {
          this.img_one_prediction = res1
          this.one_err_message = null
        }

        try {
          var res2 = await predictUrl(this.url_two)
          this.img_two_prediction = res2
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
      this.predict_load = false
    },
    swapImages() {
      let tmp = this.url_one
      this.url_one = this.url_two
      this.url_two = tmp
      tmp = this.img_one_prediction
      this.img_one_prediction = this.img_two_prediction
      this.img_two_prediction = tmp
    },
    async getRandomDog() {
      this.url_one = await this.GetRandomDogUrl()
    },
    async getRandomCat() {
      this.url_two = await this.GetRandomCatUrl()
    }
  }
}
</script>

<style scoped>
.chosen-image {
  max-height: 600px;
}
</style>
