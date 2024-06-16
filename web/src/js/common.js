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

function fillMissMonthData(data) {
  const months = data.x
  const startYM = months[0]
  let startY = parseInt(startYM.split('-')[0])
  let startM = parseInt(startYM.split('-')[1])
  const endY = new Date().getFullYear()
  const endM = new Date().getMonth() + 1 // month is 0-based
  const result = {
    x: [],
    y: []
  }
  let i = 0
  // we don't have the data of the current month
  while (startY < endY || (startY == endY && startM < endM)) {
    const m = ('0' + startM).slice(-2)
    const ym = `${startY}-${m}`
    if (months.includes(ym)) {
      result.x.push(ym)
      result.y.push(data.y[i])
      i += 1
    } else {
      result.x.push(ym)
      result.y.push(0)
    }
    startM += 1
    if (startM > 12) {
      startY += 1
      startM = 1
    }
  }
  return result
}


export default { createPaceFormatter, fillMissMonthData }
