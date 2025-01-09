$(function () {

    var $populationChart = $("#population-chart");
    var populationChart = null;

    function updatePopulationChart() {
        $.ajax({
            url: $populationChart.data("url"),
            success: function (data) {
                // console.log(data)
                if (populationChart) {
                    populationChart.updateSeries([{
                        name: 'Accept',
                        data: data.accept
                    }, {
                        name: 'Reject',
                        data: data.reject
                    }]);

                    // Cập nhật lại trục x
                    populationChart.updateOptions({
                        xaxis: {
                            categories: data.labels
                        }
                    });
                } else {
                    populationChart = new ApexCharts(document.querySelector("#population-chart"), {
                        chart: {
                            type: 'line',
                            height:400
                        },
                        series: [{
                            name: 'Accept',
                            data: data.accept
                        }, {
                            name: 'Reject',
                            data: data.reject
                        }],
                        xaxis: {
                            categories: data.labels
                        },
                        colors: ['#3692EB', '#FF6384'],
                        legend: {
                            position: 'top',
                        },
                        title: {
                            text: 'Population Line Chart',
                            align: 'left'
                        }
                    });
                    populationChart.render();
                }
            }
        });
    }

    setInterval(updatePopulationChart, 30000);
    updatePopulationChart();

});
