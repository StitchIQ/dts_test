// 路径配置
require.config({
    paths: {
        echarts: 'http://echarts.baidu.com/build/dist'
    }
});

// 使用
require(
    [
        'echarts',
        'echarts/chart/pie' // 使用pie模块，按需加载
    ],
    function (ec) {
        // 基于准备好的dom，初始化echarts图表
        var myChart = ec.init(document.getElementById('pie'));

        var option = {
            title : {
                text: '某站点用户访问来源',
                subtext: '纯属虚构',
                x:'center'
            },
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient : 'vertical',
                x : 'left',
                data:['直接访问','邮件营销','联盟广告','视频广告','搜索引擎']
            },
            toolbox: {
                show : true,
                feature : {
                    mark : {show: true},
                    dataView : {show: true, readOnly: false},
                    magicType : {
                        show: true,
                        type: ['pie', 'funnel'],
                        option: {
                            funnel: {
                                x: '25%',
                                width: '50%',
                                funnelAlign: 'left',
                                max: 1548
                            }
                        }
                    },
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            calculable : true,
            series : [
                {
                    name:'访问来源',
                    type:'pie',
                    radius : '55%',
                    center: ['50%', '60%'],
                    data:[
                        {value:335, name:'直接访问'},
                        {value:310, name:'邮件营销'},
                        {value:234, name:'联盟广告'},
                        {value:135, name:'视频广告'},
                        {value:1548, name:'搜索引擎'}
                    ],
                    itemStyle: {
                        normal: {
                            label: {
                                position:'inner',
                                formatter : function (params) {
                                  return (params.percent - 0).toFixed(0) + '%'
                                }
                            }
                        }},
                }
            ]
        };

        $(function() {
            $('tr td a').bind('click', function() {
                //alert($(this).closest('tr').find('td:eq(1)').text());
              $.getJSON("/seriousdataspie", {
                    product: $(this).closest('tr').find('td:eq(1)').text(),
                },function(data) {
                 //alert(data.date);
                 option.legend.data = data.level;
                 option.series[0].name = data.name;
                 option.series[0].data = data.data;
                 option.title.text='问题单严重程度报表pie';
                 myChart.clear();//清空绘画内容，清空后实例可用
                 myChart.hideLoading();//清除无数据时动画显示
                 myChart.setOption(option);
                 //myChart.setSeries(data.data);
                });
            });
        });
    }
);