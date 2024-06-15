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
  const distanceData = props.data.distance.data
  const paceData = props.data.pace.data
  const option = {
    grid: [
      {
        bottom: '50%'
      },
      {
        top: '60%'
      }
    ],
    title: {
      text: '距离长短自知，速度快慢随心',
      left: 'center',
    },
    xAxis: [
      {
        type: 'category',
        data: distanceData.x,
      },
      {
        type: 'category',
        data: paceData.x,
        gridIndex: 1,
      }
    ],
    yAxis:
      [
        {
          type: 'value',
          splitLine: {
            show: true
          },
        },
        {
          type: 'value',
          gridIndex: 1,
          splitLine: {
            show: true
          },
          inverse: true,
          min: 210,
          axisLabel: {
            formatter: function (d) {
              let mins = Math.floor(d / 60)
              let secs = d % 60
              secs = ('0' + secs).slice(-2)
              return mins + ':' + secs
            }
          }
        }
      ],
    series: [
      {
        data: distanceData.y,
        type: 'line',
        markLine: {
          data: [{ type: 'average', name: 'Avg' }],
          lineStyle: {
            color: 'grey'
          },
          symbol:['none', 'none'],
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
      },
      {
        data: paceData.y,
        type: 'line',
        xAxisIndex: 1,
        yAxisIndex: 1,
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
          symbol:['none', 'none'],
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
