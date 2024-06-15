function createPaceFormatter() {
  return function (params) {
    let d = params.data ? params.data.value : params
    d = Math.round(d)
    let mins = Math.floor(d / 60)
    let secs = d % 60
    secs = ('0' + secs).slice(-2)
    return mins + ':' + secs
  }
}


export default { createPaceFormatter }
