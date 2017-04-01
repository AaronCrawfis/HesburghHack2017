$(document).ready(function() {
    $("input[name$='lVenue']").click(function() {
        var test = $(this).val();
        document.getElementById('ndhLunchEntrees').style.display = 'none';
        document.getElementById('sdhLunchEntrees').style.display = 'none';

        if(test == "ndh") document.getElementById('ndhLunchEntrees').style.display = 'block';
        else if(test == "sdh") document.getElementById('sdhLunchEntrees').style.display = 'block';
    });

    $("input[name$='dVenue']").click(function() {
        var test = $(this).val();
        document.getElementById('ndhDinnerEntrees').style.display = 'none';
        document.getElementById('sdhDinnerEntrees').style.display = 'none';

        if(test == "ndh") document.getElementById('ndhDinnerEntrees').style.display = 'block';
        else if(test == "sdh") document.getElementById('sdhDinnerEntrees').style.display = 'block';
    });

    // Meal Divs -----------------------------------------------------------------------------
    $("input[name$='breakfast']").click(function() {
        var test = $(this).val();
        if(test == "yes") document.getElementById('bOptions').style.display = 'block';
        else document.getElementById('bOptions').style.display = 'none';
    });

    $("input[name$='lunch']").click(function() {
        var test = $(this).val();
        if(test == "yes") document.getElementById('lOptions').style.display = 'block';
        else document.getElementById('lOptions').style.display = 'none';
    });

    $("input[name$='dinner']").click(function() {
        var test = $(this).val();
        if(test == "yes") document.getElementById('dOptions').style.display = 'block';
        else document.getElementById('dOptions').style.display = 'none';
    });
});