import { Toast } from 'buefy/dist/components/toast'

export function SuccessNotification(message = 'Success', duration = 2000) {
  Toast.open({
    message: message,
    type: 'is-success',
    duration: duration
  })
}

export function ErrorNotification(error, duration = 2000) {
  Toast.open({
    message: error.response
      ? error.response.data.msg
      : error.message === undefined || error.message === null
        ? 'Error'
        : error.message,
    type: 'is-danger',
    duration: duration
  })
}
