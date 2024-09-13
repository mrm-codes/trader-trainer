

document.getElementById('aaplChart').classList.add('active');

function showTicker(id){

    var aapl_chart = document.getElementById('aaplChart');
    var tsla_chart = document.getElementById('tslaChart');
    var msft_chart = document.getElementById('msftChart');
    var nflx_chart = document.getElementById('nflxChart');
    
    var nvda_chart = document.getElementById('nvdaChart');
    var amzn_chart = document.getElementById('amznChart');
    var meta_chart = document.getElementById('metaChart');
    var bac_chart = document.getElementById('bacChart');

   
    
    if (id === 'aaplChart'){
        tsla_chart.classList.remove('active'); 
        nflx_chart.classList.remove('active');
        msft_chart.classList.remove('active');

        nvda_chart.classList.remove('active');
        amzn_chart.classList.remove('active');
        meta_chart.classList.remove('active');
        bac_chart.classList.remove('active');

       
        aapl_chart.classList.add('active');
    }
    else if (id === 'tslaChart'){
        aapl_chart.classList.remove('active'); 
        nflx_chart.classList.remove('active');
        msft_chart.classList.remove('active'); 

        nvda_chart.classList.remove('active');
        amzn_chart.classList.remove('active');
        meta_chart.classList.remove('active');
        bac_chart.classList.remove('active');
        
        tsla_chart.classList.add('active')
    }
    if (id === 'msftChart'){
        tsla_chart.classList.remove('active'); 
        nflx_chart.classList.remove('active');
        aapl_chart.classList.remove('active'); 

        nvda_chart.classList.remove('active');
        amzn_chart.classList.remove('active');
        meta_chart.classList.remove('active');
        bac_chart.classList.remove('active');
        
        msft_chart.classList.add('active')
    }
    if (id === 'nflxChart'){
        tsla_chart.classList.remove('active'); 
        aapl_chart.classList.remove('active');
        msft_chart.classList.remove('active');

        nvda_chart.classList.remove('active');
        amzn_chart.classList.remove('active');
        meta_chart.classList.remove('active');
        bac_chart.classList.remove('active');
        
        nflx_chart.classList.add('active')
    }

    if (id === 'nvdaChart'){
        tsla_chart.classList.remove('active'); 
        aapl_chart.classList.remove('active');
        msft_chart.classList.remove('active');

        nflx_chart.classList.remove('active');
        amzn_chart.classList.remove('active');
        meta_chart.classList.remove('active');
        bac_chart.classList.remove('active');
        
        nvda_chart.classList.add('active')
    }

    if (id === 'amznChart'){
        tsla_chart.classList.remove('active'); 
        aapl_chart.classList.remove('active');
        msft_chart.classList.remove('active');

        nvda_chart.classList.remove('active');
        nflx_chart.classList.remove('active');
        meta_chart.classList.remove('active');
        bac_chart.classList.remove('active');
        
        amzn_chart.classList.add('active')
    }

    if (id === 'metaChart'){
        tsla_chart.classList.remove('active'); 
        aapl_chart.classList.remove('active');
        msft_chart.classList.remove('active');

        nvda_chart.classList.remove('active');
        amzn_chart.classList.remove('active');
        nflx_chart.classList.remove('active');
        bac_chart.classList.remove('active');
        
        meta_chart.classList.add('active')
    }

    if (id === 'bacChart'){
        tsla_chart.classList.remove('active'); 
        aapl_chart.classList.remove('active');
        msft_chart.classList.remove('active');

        nvda_chart.classList.remove('active');
        amzn_chart.classList.remove('active');
        meta_chart.classList.remove('active');
        nflx_chart.classList.remove('active');
        
        bac_chart.classList.add('active')
    }

   
}


function settings(){
    settingsPanel = document.getElementById('settings');
    if (settingsPanel.classList.contains('set-off')){
        settingsPanel.classList.remove('set-off');
        settingsPanel.classList.add('set-on');
    } else{
        settingsPanel.classList.remove('set-on');
        settingsPanel.classList.add('set-off')
    }
}

function closeBtn(){
    settingsPanel = document.getElementById('settings');
    if (settingsPanel.classList.contains('set-on')){
        settingsPanel.classList.remove('set-on');
        settingsPanel.classList.add('set-off');
    }
}



