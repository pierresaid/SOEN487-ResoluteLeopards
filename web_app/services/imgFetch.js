import axios from 'axios'

const BaseUrl = 'http://localhost:5003/'

export async function GetRandomCatUrl() {
  try {
    let response = await axios.get(`${BaseUrl}cat`)
    return response.data.url
  } catch (error) {
    throw error
  }
}

export async function GetRandomDogUrl() {
  try {
    let response = await axios.get(`${BaseUrl}dog`)
    return response.data.url
  } catch (error) {
    throw error
  }
}
