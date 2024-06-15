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

function init(chart) {
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
      data: props.data.data.x,
    },
    yAxis: {
      type: 'value',
      inverse: true,
      min: 'dataMin',
      axisLabel: {
        formatter: function (d) {
          let mins = Math.floor(d / 60)
          let secs = d % 60
          secs = ('0' + secs).slice(-2)
          return mins + ':' + secs
        }
      }
    },
    series: [
      {
        data: props.data.data.y,
        type: 'line',
        markLine: {
          data: [{ type: 'average', name: 'Avg' }],
          label: {
            formatter: function (params) {
              let d = params.data.value
              let mins = Math.floor(d / 60)
              let secs = d % 60
              secs = ('0' + secs).slice(-2)
              return mins + ':' + secs
            }
          },
          lineStyle: {
            color: 'grey',
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
              offset: 0, color: '#1a5e1f'
            }, {
              offset: 1, color: '#81c883'
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
