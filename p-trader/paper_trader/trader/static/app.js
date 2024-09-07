

document.getElementById('aaplChart').classList.add('active');

function showTicker(id){

    var aapl_chart = document.getElementById('aaplChart');
    var tsla_chart = document.getElementById('tslaChart');
    var msft_chart = document.getElementById('msftChart');
    var nflx_chart = document.getElementById('nflxChart');

   
    
    if (id === 'aaplChart'){
        tsla_chart.classList.remove('active'); 
        nflx_chart.classList.remove('active');
        msft_chart.classList.remove('active');
        aapl_chart.classList.add('active');
    }
    else if (id === 'tslaChart'){
        aapl_chart.classList.remove('active'); 
        nflx_chart.classList.remove('active');
        msft_chart.classList.remove('active'); 
        tsla_chart.classList.add('active')
    }
    if (id === 'msftChart'){
        tsla_chart.classList.remove('active'); 
        nflx_chart.classList.remove('active');
        aapl_chart.classList.remove('active'); 
        msft_chart.classList.add('active')
    }
    if (id === 'nflxChart'){
        tsla_chart.classList.remove('active'); 
        aapl_chart.classList.remove('active');
        msft_chart.classList.remove('active');
        nflx_chart.classList.add('active')
    }
}








