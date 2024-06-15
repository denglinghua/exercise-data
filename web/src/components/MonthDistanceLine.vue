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
      type: 'value'
    },
    series: [
      {
        data: props.data.data.y,
        type: 'line',
        markLine: {
          data: [{ type: 'average', name: 'Avg' }],
          lineStyle: {
            color: 'grey'
          },
        },
        lineStyle: {
          color: 'Orange'
        },
        showSymbol: false
      }
    ]
  };

  chart.setOption(option);

}
</script>
