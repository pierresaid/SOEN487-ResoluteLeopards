import { ErrorNotification } from '../helpers/Notifications'

const BaseUrl = 'http://localhost:5003/'

export const state = () => ({
  dogs_urls: [
    'https://i.imgur.com/pCFB7G2.jpg',
    'https://i.imgur.com/M1Hsxs0.jpg',
    'https://i.imgur.com/A9XNHzo.jpg',
    'https://i.imgur.com/5gU8OF4.jpg',
    'https://i.imgur.com/yiHC0gL.jpg',
    'https://i.imgur.com/QnXlHJW.jpg',
    'https://i.imgur.com/gsh3Zod.jpg',
    'https://i.imgur.com/cPgqDsY.jpg',
    'https://i.imgur.com/sio3Td8.jpg',
    'https://i.imgur.com/pz2ljmu.jpg',
    'https://i.imgur.com/sHMzHNc.jpg',
    'https://i.imgur.com/Z3mpgWD.jpg',
    'https://i.imgur.com/dTefEgp.jpg',
    'https://i.imgur.com/UgdrPif.jpg',
    'https://i.imgur.com/39vh889.jpg',
    'https://i.imgur.com/kgrKfA1.jpg',
    'https://i.imgur.com/s0z7DNN.jpg',
    'https://i.imgur.com/KytqvoF.jpg',
    'https://i.imgur.com/0N6n8Fz.jpg',
    'https://i.imgur.com/vH7lboK.jpg',
    'https://i.imgur.com/Dx4Ozm3.jpg',
    'https://i.imgur.com/VTyjZ2g.jpg',
    'https://i.imgur.com/SIzsaV9.jpg',
    'https://i.imgur.com/5So9nSk.jpg',
    'https://i.imgur.com/xocMLaz.jpg',
    'https://i.imgur.com/vN6yz0V.jpg',
    'https://i.imgur.com/DMA0xRp.jpg',
    'https://i.imgur.com/ng25itv.jpg',
    'https://i.imgur.com/fjm0TiC.jpg',
    'https://i.imgur.com/ppExyGB.jpg',
    'https://i.imgur.com/48m9iJ1.jpg',
    'https://i.imgur.com/JgZ0CvH.jpg',
    'https://i.imgur.com/s1l5k1s.jpg',
    'https://i.imgur.com/cL0644A.jpg',
    'https://i.imgur.com/41b1E2y.jpg',
    'https://i.imgur.com/WCO5G8W.jpg',
    'https://i.imgur.com/VQCVTQC.jpg',
    'https://i.imgur.com/YXZ7icj.jpg',
    'https://i.imgur.com/oI1F3nJ.jpg',
    'https://i.imgur.com/dF3bJEO.jpg',
    'https://i.imgur.com/DUXmbi2.jpg',
    'https://i.imgur.com/n81jKuC.jpg',
    'https://i.imgur.com/ZGi03rW.jpg',
    'https://i.imgur.com/oOjQ7bD.jpg',
    'https://i.imgur.com/74Lv399.jpg',
    'https://i.imgur.com/Q9tqHoR.jpg',
    'https://i.imgur.com/O9Iz2Kk.jpg',
    'https://i.imgur.com/xbkBxz9.jpg',
    'https://i.imgur.com/JcEiYOs.jpg',
    'https://i.imgur.com/XMPNyFt.jpg',
    'https://i.imgur.com/DqZam5j.jpg',
    'https://i.imgur.com/YLHgd6l.jpg',
    'https://i.imgur.com/mIKBWyR.jpg',
    'https://i.imgur.com/ShJTlO0.jpg',
    'https://i.imgur.com/qs4PYZQ.jpg',
    'https://i.imgur.com/LwHK15F.jpg',
    'https://i.imgur.com/LMuEDxG.jpg',
    'https://i.imgur.com/lXIlf3v.jpg',
    'https://i.imgur.com/KEcbsz9.jpg',
    'https://i.imgur.com/WGcScNm.jpg',
    'https://i.imgur.com/fohu7EF.jpg',
    'https://i.imgur.com/CXdGGre.jpg',
    'https://i.imgur.com/2wr71CL.jpg',
    'https://i.imgur.com/9qSxCcS.jpg',
    'https://i.imgur.com/S3BOUuJ.jpg',
    'https://i.imgur.com/sHSGpyX.jpg',
    'https://i.imgur.com/goaB0KQ.jpg',
    'https://i.imgur.com/9ITZtY1.jpg',
    'https://i.imgur.com/s69AZKW.jpg',
    'https://i.imgur.com/DE6ivym.jpg',
    'https://i.imgur.com/LgHMnuy.jpg',
    'https://i.imgur.com/dXMqVKr.jpg',
    'https://i.imgur.com/lyExt5B.jpg',
    'https://i.imgur.com/3m96JBp.jpg',
    'https://i.imgur.com/xAA0WZ2.jpg',
    'https://i.imgur.com/fpdirVN.jpg',
    'https://i.imgur.com/MN77nTQ.jpg',
    'https://i.imgur.com/jW8Br7v.jpg',
    'https://i.imgur.com/2K9edFI.jpg',
    'https://i.imgur.com/igANmJu.jpg',
    'https://i.imgur.com/iXykC1t.jpg',
    'https://i.imgur.com/qdGlYJa.jpg',
    'https://i.imgur.com/GPCiIL2.jpg',
    'https://i.imgur.com/BZHkPA1.jpg',
    'https://i.imgur.com/9MIG5nI.jpg'
  ],
  dogs_page: 0,
  cats_urls: [],
  cats_page: 0,
  fetching: false
})

export const mutations = {
  SET_FETCHING_DOGS(state, status) {
    state.fetching = status
  },
  ADD_URLS_DOGS(state, urls) {
    for (let i = 0; i < urls.length; i++) {
      state.dogs_urls.push(urls[i])
    }
    state.dogs_page += 1
  },
  SET_FETCHING_CATS(state, status) {
    state.fetching = status
  },
  ADD_URLS_CATS(state, urls) {
    for (let i = 0; i < urls.length; i++) {
      state.cats_urls.push(urls[i])
    }
    state.cats_page += 1
  }
}

export const actions = {
  async GetDogs({ state, commit }) {
    commit('SET_FETCHING_DOGS', true)
    try {
      let response = await this.$axios.$get(
        BaseUrl + `imgur/dog/${state.dogs_page}`,
        { progress: false }
      )
      commit('ADD_URLS_DOGS', response.images)
    } catch (error) {
      ErrorNotification(error)
    }
    commit('SET_FETCHING_DOGS', false)
  }
}
