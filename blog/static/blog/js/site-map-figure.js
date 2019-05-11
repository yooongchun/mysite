//关于页面map数据请求
$(document).ready(function () {
    if ($("title").text() === "关于") {
        let TYPE_FOR_QUERY_MAP_DATA = 'QUERY_FOR_MAP_DATA'; //关于页面map数据请求标志
        $.get("", {"type": TYPE_FOR_QUERY_MAP_DATA}, function (data, status) {
            let res = [];
            let data_list = data.split('}{');
            if (data_list.length <= 1) {
                res.push(eval('(' + data_list + ')'));
            } else {
                let first = data_list[0];
                let last = data_list[data_list.length - 1];
                for (let d of data_list) {
                    if (d === first) {
                        res.push(eval('(' + d + '}' + ')'));
                    } else if (d === last) {
                        res.push(eval('(' + '{' + d + ')'));
                    } else {
                        res.push(eval('(' + '{' + d + '}' + ')'));
                    }
                }
            }
            let datas = convertData(res);
            let max = datas[1];
            let data1 = datas[0];
            drawMap(data1, max, $('.site-map')[0]);
        });
    }
});

function convertData(data) {
    let ndata = [];
    let arr = [];
    for (let d of data) {
        arr.push(Number(d['num']));
    }
    let max = Math.max.apply(null, arr);
    for (let d of data) {
        ndata.push({name: d['name'], value: [Number(d['lng']), Number(d['lat']), Number(d['num'])]});
    }
    return [ndata, max];

}

function drawMap(data, max, dom) {
    let MAX_SYMBOL_SIZE = 30;//定义最大symbol尺寸
    let myChart = echarts.init(dom);
    option = {
        title: {
            text: '访问本站的小伙伴来自这些地方~',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        bmap: {
            center: [110.114129, 34.550339],
            zoom: 6,
            roam: true,
            mapStyle: {
                styleJson: [{
                    'featureType': 'water',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#d1d1d1'
                    }
                }, {
                    'featureType': 'land',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#f3f3f3'
                    }
                }, {
                    'featureType': 'railway',
                    'elementType': 'all',
                    'stylers': {
                        'visibility': 'off'
                    }
                }, {
                    'featureType': 'highway',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#fdfdfd'
                    }
                }, {
                    'featureType': 'highway',
                    'elementType': 'labels',
                    'stylers': {
                        'visibility': 'off'
                    }
                }, {
                    'featureType': 'arterial',
                    'elementType': 'geometry',
                    'stylers': {
                        'color': '#fefefe'
                    }
                }, {
                    'featureType': 'arterial',
                    'elementType': 'geometry.fill',
                    'stylers': {
                        'color': '#fefefe'
                    }
                }, {
                    'featureType': 'poi',
                    'elementType': 'all',
                    'stylers': {
                        'visibility': 'off'
                    }
                }, {
                    'featureType': 'green',
                    'elementType': 'all',
                    'stylers': {
                        'visibility': 'off'
                    }
                }, {
                    'featureType': 'subway',
                    'elementType': 'all',
                    'stylers': {
                        'visibility': 'off'
                    }
                }, {
                    'featureType': 'manmade',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#d1d1d1'
                    }
                }, {
                    'featureType': 'local',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#d1d1d1'
                    }
                }, {
                    'featureType': 'arterial',
                    'elementType': 'labels',
                    'stylers': {
                        'visibility': 'off'
                    }
                }, {
                    'featureType': 'boundary',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#fefefe'
                    }
                }, {
                    'featureType': 'building',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#d1d1d1'
                    }
                }, {
                    'featureType': 'label',
                    'elementType': 'labels.text.fill',
                    'stylers': {
                        'color': '#999999'
                    }
                }]
            }
        },
        series: [
            {
                name: '访问量',
                type: 'effectScatter',
                coordinateSystem: 'bmap',
                data: data,
                symbolSize: function (val) {
                    return val[2] * MAX_SYMBOL_SIZE / max+5;
                },
                label: {
                    normal: {
                        formatter: '',
                        position: 'right',
                        show: true,
                    },
                    emphasis: {
                        show: true
                    }
                },
                itemStyle: {
                    normal: {
                        color: 'purple'
                    }
                },
                tooltip: {
                    formatter: function (params, ticket, callback) {
                        return params.seriesName + '<br/>' + params.name + ':&nbsp;' + params.value[2].toString() + '人';
                    },
                },
            },
            {
                name: 'Top5',
                type: 'effectScatter',
                coordinateSystem: 'bmap',
                data: (data.sort(function (a, b) {
                    return b.value[2] - a.value[2];
                }).slice(0, 5)),
                symbolSize: function (val) {
                    return val[2] * MAX_SYMBOL_SIZE / max+5;
                },
                showEffectOn: 'render',
                rippleEffect: {
                    brushType: 'stroke'
                },
                hoverAnimation: true,
                label: {
                    normal: {
                        formatter: '{b}',
                        position: 'right',
                        show: false
                    }
                },
                itemStyle: {
                    normal: {
                        color: 'purple',
                        shadowBlur: 10,
                        shadowColor: '#333'
                    }
                },
                zlevel: 1,
                tooltip: {
                    formatter: function (params, ticket, callback) {
                        return params.seriesName + '<br/>' + params.name + ':&nbsp;' + params.value[2].toString() + '人';
                    },
                },
            }
        ]
    };
    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }
}