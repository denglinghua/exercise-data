import common from "./common.js";
import chart from "./chart.js";
import "echarts-wordcloud";

function activityTimePie(data) {
  const series = data.series.map((item) => {
    return { name: item[0], value: item[1] };
  });
  let option = {
    title: {
      text: data.title,
      left: "center",
    },
    tooltip: {
      trigger: "item",
      valueFormatter: common.createMins2HoursFormatter(),
    },
    color: ["red", "blue", "green"],
    series: [
      {
        type: "pie",
        radius: ["40%", "70%"],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: "#fff",
          borderWidth: 2,
        },
        label: {
          formatter: common.createMins2HoursFormatter(),
          color: "inherit",
          fontSize: 14,
          fontStyle: "bold",
        },
        data: series,
      },
    ],
  };
  return option;
}

function monthActivityFreqAreaLine(data) {
  const actitities = ["Running", "Swimming", "Cycling"];
  const orderSeries = data.series.sort((a, b) => a[0].localeCompare(b[0]));
  let x = [];
  let series = [];
  for (let a of actitities) {
    series.push({
      name: a,
      type: "line",
      stack: "total",
      showSymbol: false,
      areaStyle: {},
      data: [],
    });
  }

  for (let s of orderSeries) {
    x.push(s[0]);
    for (let i = 0; i < series.length; i++) {
      series[i].data.push(s[1][i]);
    }
  }

  const option = {
    title: {
      text: data.title,
      left: "center",
    },
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "cross",
        label: {
          backgroundColor: "#6a7985",
        },
      },
    },
    legend: {
      data: actitities,
      bottom: 20,
    },
    xAxis: [
      {
        type: "category",
        boundaryGap: false,
        data: x,
      },
    ],
    yAxis: [
      {
        type: "value",
      },
    ],
    series: series,
  };

  return option;
}

function runPlaceWordCloud(data) {
  const series = data.series.map((item) => {
    return { name: item[0], value: item[1] };
  });
  const option = {
    title: {
      text: data.title,
      left: "center",
    },
    tooltip: {
      show: true,
    },
    color: [
      "#5470c6",
      "#91cc75",
      "#fac858",
      "#ee6666",
      "#73c0de",
      "#3ba272",
      "#fc8452",
      "#9a60b4",
      "#ea7ccc",
    ],
    series: [
      {
        type: "wordCloud",
        shape: "diamond",
        gridSize: 2,
        sizeRange: [16, 80],
        rotationRange: [0, 0],
        layoutAnimation: true,
        textStyle: {
          fontFamily: "sans-serif",
          color: function () {
            return (
              "rgb(" +
              [
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160),
              ].join(",") +
              ")"
            );
          },
        },
        data: series,
      },
    ],
  };
  return option;
}

function weekHourHeatmap(data) {
  return chart.weekHourHeatmap(data, ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]);
}

export default {
  activityTimePie,
  monthActivityFreqAreaLine,
  runPlaceWordCloud,
  weekHourHeatmap,
};
