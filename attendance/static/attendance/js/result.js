$(function () {
   $("#table-75").hide();

   $("#average").html("Avg : " + avgPerc().toFixed(2) +"%");

   addExtrasToList();

   drawgraph1();
   drawgraph2();

   if (isEmpty(list80)){
       $("#graph80").hide();
       $("#graphAtd").addClass("col-md-offset-2");
   }

   if (isEmpty(list75)) {
       $("#graph75").hide();
       $("#graphAtd").addClass("col-md-offset-2");
   }

   if (isEmpty(list80) && isEmpty(list75)){
       $("#graphAtd").removeClass("col-md-offset-2");
       $("#graphAtd").addClass("col-md-offset-4");
   }
});

var avgPerc = function () {
    var avg = 0;
    var i;
    for(i =0 ; i < testdata.length ; i++) {
        avg += parseFloat(testdata[i]);
        console.log("Adding to avg " + testdata[i]);
    }
    console.log("Dividing " + avg + " with " + testdata.length);
    return parseFloat(avg)/parseFloat((testdata.length));
};


var addExtrasToList = function() {

    for(i =testdata.length - 1 ; i >= 0 ; i--) {
        testdata[i+1] = testdata[i];
        labels_sem_list[i+1] = labels_sem_list[i];
        list80[i+1] = list80[i];
        list75[i+1] = list75[i];
    }

    testdata[0] = "0";
    testdata[testdata.length] = "0";

    labels_sem_list[0] = "0";
    labels_sem_list[labels_sem_list.length] = "0";

    list80[0] = 0;
    list80[list80.length] = 0;

    list75[0] = 0;
    list75[list75.length] = 0;
};

var time = 0;

var isEmpty = function(list){
  var result = true;

  for(i = 0; i < list.length; i++){
      if(list[i] === 0) {
      }else{
          result = false;
          return result;
      }
  }
  return result;
};

$("#75-btn").bind('click', function (event) {
    $(this).addClass('active');
    $('#80-btn').removeClass('active');
    $('#table-80').hide(time);
    $('#table-75').show(time);
});

$("#80-btn").bind('click', function (event) {
    $(this).addClass('active');
    $('#75-btn').removeClass('active');
    $('#table-75').hide(time);
    $('#table-80').show(time);
});

var drawgraph1 = function() {


    var ctx = $("#attendance");
    var myChart = new Chart(ctx, {
    type: 'bar',
    data: {

            labels: labels_sem_list,
            datasets: [{
                type: 'bar',
                data: testdata,
                backgroundColor: [
                    '',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    '',
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderWidth: 1
            },
            {
                type: 'line',
                label: '80%',
                data: Array.apply(null, new Array(testdata.length)).map(Number.prototype.valueOf, 80),
                fill: false,
                radius: 0,
                backgroundColor: 'rgba(246, 106, 124, 0.82)',
                borderColor: 'rgba(246, 106, 124, 0.82)'
            },
            {
                type: 'line',
                label: '80%',
                data: Array.apply(null, new Array(testdata.length)).map(Number.prototype.valueOf, 75),
                fill: false,
                radius: 0,
                backgroundColor: 'rgba(106, 216, 246, 0.82)',
                borderColor: 'rgba(106, 216, 246, 0.82)'
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }],
                xAxes: [{
                    display: false
                }]
            },
            legend: {
                display: false,
                labels: {
                    display: false
                }
            }
        }
    });

};

var drawgraph2 = function(){

    var ctx2 = $("#requiredClasses");
    var ctx3 = $("#requiredClasses2");
    var data = {
        labels: labels_sem_list,
        datasets: [
            {
                data: list80,
                backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255,0.8)',
                        'rgba(255, 159, 64, 0.8)',
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255,0.8)',
                        'rgba(255, 159, 64, 0.8)'
                ],
                hoverBackgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255,0.8)',
                        'rgba(255, 159, 64, 0.8)',
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255,0.8)',
                        'rgba(255, 159, 64, 0.8)'
                ]
            }]
        };

    var data2 = {
        labels: labels_sem_list,
        datasets: [
            {
                data: list75,
                backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255,0.8)',
                        'rgba(255, 159, 64, 0.8)',
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255,0.8)',
                        'rgba(255, 159, 64, 0.8)'
                ],
                hoverBackgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255,0.8)',
                        'rgba(255, 159, 64, 0.8)',
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255,0.8)',
                        'rgba(255, 159, 64, 0.8)'
                ]
            }]
        };


    var myPieChart = new Chart(ctx2,{
    type: 'pie',
    data: data,
    options: {
            legend: {
                display: false,
                labels: {
                    display: false
                }
            },
        }
    });

    var myPieChart = new Chart(ctx3,{
    type: 'pie',
    data: data2,
    options: {
            legend: {
                display: false,
                labels: {
                    display: false
                }
            }
        }
    });
};