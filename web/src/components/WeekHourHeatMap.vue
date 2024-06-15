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
  const hours = [
    '12A', '1A', '2A', '3A', '4A', '5A', '6A',
    '7A', '8A', '9A', '10A', '11A',
    '12P', '1P', '2P', '3P', '4P', '5P',
    '6P', '7P', '8P', '9P', '10P', '11P'
  ];
  const days = [
    '一', '二', '三', '四', '五', '六', '日'
  ];
  const data = props.data.data
  const option = {
    title: {
      text: props.data.title,
      left: 'center',
    },
    tooltip: {
      position: 'top',
    },
    grid: {
      height: '50%',
      top: '10%'
    },
    xAxis: {
      type: 'category',
      data: hours,
      splitArea: {
        show: true
      }
    },
    yAxis: {
      type: 'category',
      data: days,
      splitArea: {
        show: true
      }
    },
    visualMap: {
      min: 0,
      max: 10,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '15%'
    },
    series: [
      {
        type: 'heatmap',
        data: data,
        label: {
          show: true
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  };

  chart.setOption(option);
}
</script>
