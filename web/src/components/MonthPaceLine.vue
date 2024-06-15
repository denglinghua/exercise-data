<template>
  <ChartBase :init="init" :data="data" />
</template>
<script setup>
import { ref, watch, defineProps, onMounted } from 'vue'
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
            color: 'grey'
          },
        },
        lineStyle: {
          color: 'Green'
        },
        showSymbol: false
      }
    ]
  };

  chart.setOption(option);

}
</script>
