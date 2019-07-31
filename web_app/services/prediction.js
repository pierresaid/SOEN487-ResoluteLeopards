import axios from 'axios'

const BaseUrl = 'https://ml.api.cat-vs-dog.said.tech/'

export default async function predictUrl(url) {
  try {
    let response = await axios.get(`${BaseUrl}predict`, {
      params: {
        url: url
      }
    })
    return { label: response.data.label, percentage: response.data.prediction }
  } catch (error) {
    throw error.response !== undefined
      ? error.response.data.message
      : new Error('Service unreachable')
  }
}
