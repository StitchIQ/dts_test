
    // 基于准备好的dom，初始化echarts图表
    var dailycharts = echarts.init(document.getElementById('daily'));
    var softwarecharts = echarts.init(document.getElementById('software'));
    var featurescharts = echarts.init(document.getElementById('features'));
    var seriouscharts = echarts.init(document.getElementById('serious'));
    var statuscharts = echarts.init(document.getElementById('status'));
    var authorcharts = echarts.init(document.getElementById('author'));

    var option = {
        title : {
            text: '',
            //subtext: '纯属虚构'
        },
        tooltip: {
            show: true
        },
        legend: {
            data:['Bugs']
        },
        toolbox: {
            show : true,
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                magicType : {show: true, type: ['line', 'bar']},
                restore : {show: true},
                //saveAsImage : {show: true}
            }
        },
         xAxis : [
            {
                type : 'category',
                data : [],
                axisLabel:{
                    interval:0,
                    rotate:30,//倾斜度 -90 至 90 默认为0
                    margin:2,
                    textStyle:{
                        fontWeight:"bolder",
                        color:"#000000"
                    }
                },
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],
        series : [{name:'',type:'bar',data:[],
        itemStyle: {
                    normal: {
                        label: {
                            show: true,//是否展示
                            position:'inside'
                        }
                    }},
        }]
    };

    $(function() {
        $("tr td a").on("click", function() {
            var para = $(this).text();

          $.getJSON("/bugdailydatas", {
                product: para,
            },
            function(data) {
             //alert(data.date);
             option.xAxis[0].data = data.dataX;
             option.series[0].name = data.name;
             option.series[0].data = data.dataY;
             option.title.text = "问题单版本分布报表";
             dailycharts.clear();//清空绘画内容，清空后实例可用
             dailycharts.hideLoading();//清除无数据时动画显示
             dailycharts.setOption(option,true);
             //myChart.setSeries(data.data);
            });

          $.getJSON("/softwarebugdatas", {
                product: para,
            },
            function(data) {
             //alert(data.date);
             option.xAxis[0].data = data.dataX;
             option.series[0].name = data.name;
             option.series[0].data = data.dataY;
             option.title.text = "问题单版本分布报表";
             softwarecharts.clear();//清空绘画内容，清空后实例可用
             softwarecharts.hideLoading();//清除无数据时动画显示
             softwarecharts.setOption(option,true);
             //myChart.setSeries(data.data);
            });

            $.getJSON("/featuresbugdatas",
                { product: para, },
                function(data) {
                     //alert(data.date);
                     option.xAxis[0].data = data.dataX;
                     option.series[0].name = data.name;
                     option.series[0].data = data.dataY;
                     option.title.text = "问题单特性分布报表";
                     featurescharts.clear();//清空绘画内容，清空后实例可用
                     featurescharts.hideLoading();//清除无数据时动画显示
                     featurescharts.setOption(option,true);
                     //myChart.setSeries(data.data);
                });

            $.getJSON("/seriousbugdatas",
                { product: para, },
                function(data) {
                     //alert(data.date);
                     option.xAxis[0].data = data.dataX;
                     option.series[0].name = data.name;
                     option.series[0].data = data.dataY;
                     option.title.text = "问题单严重程度报表";
                     seriouscharts.clear();//清空绘画内容，清空后实例可用
                     seriouscharts.hideLoading();//清除无数据时动画显示
                     seriouscharts.setOption(option,true);
                     //myChart.setSeries(data.data);
                });

            $.getJSON("/statusbugdatas",
                { product: para, },
                function(data) {
                     //alert(data.date);
                     option.xAxis[0].data = data.dataX;
                     option.series[0].name = data.name;
                     option.series[0].data = data.dataY;
                     option.title.text = "问题单状态报表";
                     statuscharts.clear();//清空绘画内容，清空后实例可用
                     statuscharts.hideLoading();//清除无数据时动画显示
                     statuscharts.setOption(option,true);
                     //myChart.setSeries(data.data);
                });

            $.getJSON("/authorbugsdatas",
                { product: para, },
                function(data) {
                     //alert(data.date);
                     option.xAxis[0].data = data.dataX;
                     option.series[0].name = data.name;
                     option.series[0].data = data.dataY;
                     option.title.text = "问题单提交人员报表";
                     authorcharts.clear();//清空绘画内容，清空后实例可用
                     authorcharts.hideLoading();//清除无数据时动画显示
                     authorcharts.setOption(option,true);
                     //myChart.setSeries(data.data);
                });
        });
    });
