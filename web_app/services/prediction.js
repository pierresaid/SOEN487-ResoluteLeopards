import axios from 'axios'

const BaseUrl = 'http://localhost:5002/'

export default async function predictUrl(url) {
  let response = await axios.get(`${BaseUrl}predict?url=${url}`)
  return response.data.prediction
}
