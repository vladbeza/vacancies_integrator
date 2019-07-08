function addChart(title, series, categories, xTitle, yTitle, chartType, divId){

        if (chartType === "column")
        {
            var tooltip = {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="padding:0">jobs count: </td>' +
                '<td style="padding:0"><b>{point.y}</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
           };

           var plotOptions = {
                column: {
                    pointPadding: 0,
                    borderWidth: 0,
                    groupPadding: 0,
                    shadow: false
                }
            };
        }
        else
        {
            var tooltip = {
                crosshairs: true,
                shared: true
            };

            var plotOptions = {};
        }


        document.addEventListener('DOMContentLoaded', function () {
            var myChart = Highcharts.chart(divId, {
        chart: {
            type: chartType
        },
        tooltip: {
                crosshairs: true,
                shared: true
            },
        title: {
            text: title
        },
        xAxis: {
            title: {
                text: xTitle
            },
            categories: categories
        },
        yAxis: {
            min: 0,
            title: {
                text: yTitle
            }
        },
        tooltip: tooltip,
        plotOptions: plotOptions,
        series: series
        });
    });
   }