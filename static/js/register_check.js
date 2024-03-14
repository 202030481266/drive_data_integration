let check_box = document.getElementsByClassName('checkbox');
let password1 = document.getElementsByName('verify_password');
let password2 = document.getElementsByName('password')
let username = document.getElementsByName('username');

check_box = check_box[0];
password1 = password1[0];
password2 = password2[0];
username = username[0];


function check_form() {
    if(check_box.checked === false){
        alert("请先阅读并同意《用户注册协议》！");
        return false;
    }
    else if(password2.value !== password1.value) {
        alert("密码不一致");
        return false;
    }
    else if(username.value.length < 1 || username.value.length > 60) {
        alert("用户名长度不合法，太短或者太长。");
        return false;
    }
    else if(password1.value.length < 8) {
        alert("密码强度太弱，最多30位，最少8位");
        return false;
    }
    else if(password1.value.length > 30) {
        alert("密码强度太弱，最多30位，最少8位");
        return false;
    }
    // else if(contact.value.length > 30) {
    //     console.log(contact.value)
    //     alert("联系方式过长，建议使用其他的联系方式");
    //     return false;
    // }
    return true;
}

function dateStart()
{
    let i;
    //月份对应天数
    MonHead = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

    //给年下拉框赋内容
    const y = new Date().getFullYear();
    for (i = (y-50); i < (y+50); i++) //以今年为准，前50年，后50年
        document.date.year.options.add(new Option(" "+ i +" 年", i));

    //给月下拉框赋内容
    for (i = 1; i < 13; i++)
        document.date.month.options.add(new Option(" " + i + " 月", i));

    document.date.year.value = y;
    document.date.month.value = new Date().getMonth() + 1;
    let n = MonHead[new Date().getMonth()];
    if ( new Date().getMonth() ==1 && IsPinYear(yearvalue) )
        n++;
    writeDay(n); //赋日期下拉框
    document.date.day.value = new Date().getDate();
}

if(document.attachEvent)
    window.attachEvent("onload", dateStart);
else
    window.addEventListener('load', dateStart, false);

function selectYear(str) //年发生变化时日期发生变化(主要是判断闰平年)
{
    const monthvalue = document.date.month.options[document.date.month.selectedIndex].value;
    if (monthvalue == "")
    {
        const e = document.date.day;
        optionsClear(e);
        return;
    }
    let n = MonHead[monthvalue - 1];
    if ( monthvalue ==2 && IsPinYear(str) )
        n++;
    writeDay(n);
}

function selectMonth(str) //月发生变化时日期联动
{
    const yearvalue = document.date.year.options[document.date.year.selectedIndex].value;
    if (yearvalue == "")
    {
        const e = document.date.day;
        optionsClear(e);
        return;
    }
    let n = MonHead[str - 1];
    if ( str ==2 && IsPinYear(yearvalue) )
        n++;
    writeDay(n);
}

function writeDay(n) //据条件写日期的下拉框
{
    const e = document.date.day;
    optionsClear(e);
    for (let i=1; i<(n+1); i++)
        e.options.add(new Option(" "+ i + " 日", i));
}

function IsPinYear(year)//判断是否闰平年
{
    return( 0 === year%4 && ( year%100 !==0 || year%400 === 0 ) );
}

function optionsClear(e)
{
    e.options.length = 1;
}
