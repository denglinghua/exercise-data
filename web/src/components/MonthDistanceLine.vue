<template>
  <ChartBase :init="init" :data="data" />
</template>
<script setup>
import { defineProps } from 'vue'
import ChartBase from 'src/components/ChartBase.vue'

const props = defineProps({
  data: {
    type: Object,
  },
})

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

function init(chart) {
  const data = fillMissMonthData(props.data.data)
  const option = {
    title: {
      text: props.data.title,
      left: 'center',
    },
    tooltip: {
      trigger: 'axis',
    },
    xAxis: {
      type: 'category',
      data: data.x,
    },
    yAxis: {
      type: 'value'
    },
    grid: {
      left: '8%',
      right: '2%',
    },
    series: [
      {
        data: data.y,
        type: 'line',
        markLine: {
          data: [{ type: 'average', name: 'Avg' }],
          lineStyle: {
            color: 'grey'
          },
          label: {
            position: 'insideEndTop',
          },
          symbol: ['none', 'none'],
        },
        lineStyle: {
          color: {
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            type: 'linear',
            colorStops: [{
              offset: 0, color: '#e65104'
            }, {
              offset: 1, color: '#ffb74c'
            }],
            global: false
          }
        },
        showSymbol: false
      }
    ]
  };

  chart.setOption(option);

}
</script>
