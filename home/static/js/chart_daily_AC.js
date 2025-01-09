console.log(chart_data)
var options = {
    chart: {
        type: 'bar', // Loại biểu đồ
       // Chiều cao của biểu đồ
    },
    series: [{
        name: 'Accept', // Nhãn cho dữ liệu Accept
        data: chart_data.ac // Dữ liệu Accept
    }, {
        name: 'Reject', // Nhãn cho dữ liệu Reject
        data: chart_data.rj // Dữ liệu Reject
    }],
    xaxis: {
        categories: chart_data.hours // Các nhãn trục x
    },
    plotOptions: {
        bar: {
            horizontal: false // Sắp xếp cột theo chiều ngang
        }
    },
    dataLabels: {
        enabled: false // Tắt hiển thị nhãn dữ liệu trên cột
    },
    colors: ['#3692EB', '#FF6384'], // Màu sắc cho Accept và Reject
    legend: {
        position: 'top', // Vị trí của chú thích
        horizontalAlign: 'left', // Canh chỉnh ngang
        fontSize: '16px' // Kích thước chữ
    }
};

// Tạo biểu đồ ApexCharts
var chart = new ApexCharts(document.querySelector("#daily_chart_AC"), options);

// Vẽ biểu đồ
chart.render();