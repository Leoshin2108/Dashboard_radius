$(function () {

    var $Chart = $("#chart_AC_RJ");
    var chart = null;

    function updateChart() {
        $.ajax({
            url: $Chart.data("url"),
            success: function (data) {
                var series = [{
                    name: 'Accept',
                    data: [data.ac]
                }, {
                    name: 'Reject',
                    data: [data.rj]
                }];
                
                if (!chart) {
                    var options = {
                        chart: {
                            type: 'bar',
                            height: 400
                        },
                        series: series,
                        xaxis: {
                            categories: ['Accept/Reject']
                        },
                        plotOptions: {
                            bar: {
                                horizontal: false
                            }
                        },
                        dataLabels: {
                            enabled: false
                        },
                        colors: ['#FF6384', '#FF9F40'],
                        legend: {
                            position: 'top',
                        },
                        title: {
                            text: 'Accept/Reject Bar Chart',
                            align: 'left'
                        },
                        yaxis: {
                            title: {
                                text: 'Count'
                            }
                        }
                    };
                    chart = new ApexCharts(document.querySelector("#chart_AC_RJ"), options);
                    chart.render();
                } else {
                    chart.updateSeries(series);
                }
            }
        });
    }

    setInterval(updateChart, 30000); // Cập nhật mỗi 30 giây
    updateChart(); // Khởi chạy cập nhật ban đầu

});
