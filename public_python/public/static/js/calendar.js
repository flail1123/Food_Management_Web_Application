const date = new Date();
let lastDay;

const renderCalendar = () => {
    date.setDate(1);
    
    const monthDays = document.querySelector(".calendar-days")
    
    lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
    
    let firstDayIndex = date.getDay();
    if (firstDayIndex == 0) {
        firstDayIndex = 7;
    }
    const prevMonthLastDay = new Date(date.getFullYear(), date.getMonth(), 0).getDate();
    const lastDayIndex = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDay();

    let nextDays;
    if (lastDayIndex == 0) {
        nextDays = 0;
    }
    else {
        nextDays = 7 - lastDayIndex;
    }

    
    const months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ];
    
    document.querySelector(".calendar-date h1").innerHTML = months[date.getMonth()]
    
    document.querySelector(".calendar-date p").innerHTML = date.getFullYear();
    
    let days = "";
    
    for (let x = firstDayIndex - 1; x > 0; x--) {
        days += `<div class="calendar-prev-date">${prevMonthLastDay - x + 1}</div>`
    }
    
    for (let i = 1; i <= lastDay; i++) {
        if (i === new Date().getDate() && date.getMonth() === new Date().getMonth()) {
            days += `<div class="calendar-today d${i}" onclick="callForm(${i})">${i}</div>`
        }
        else {
            days += `<div class="d${i}" onclick="callForm(${i})">${i}</div>`
        }        
    }
    
    for (let j = 1; j <= nextDays; j++) {
        days += `<div class="calendar-next-date">${j}</div>`
    }
    
    monthDays.innerHTML = days;
}

function callForm(x) {
    document.getElementById('f_day').value = `${x}`;
    document.getElementById('f_month').value = `${date.getMonth() + 1}`;
    document.getElementById('f_year').value = `${date.getFullYear()}`;
    document.getElementById('loadDate').submit();
}

/*const makeListeners = () => {
    console.log(lastDay);
    for (i = 1; i <= lastDay; ++i) {
        try {
            document.querySelector(`.d${i}`).addEventListener('click', () => {
                console.log();
                document.getElementById('f_day').value = `${i}`;
                document.getElementById('f_month').value = `${date.getMonth() + 1}`;
                document.getElementById('f_year').value = `${date.getFullYear()}`;
                document.getElementById('loadDate').submit();
            })
        }
        catch (error) {
            console.error(error);
        }
    }
}*/

document.querySelector('.calendar-prev').addEventListener('click', () => {
    date.setMonth(date.getMonth() - 1);
    renderCalendar();
    //makeListeners();
})

document.querySelector('.calendar-next').addEventListener('click', () => {
    date.setMonth(date.getMonth() + 1);
    renderCalendar();
    //makeListeners();
})

renderCalendar();
//makeListeners();