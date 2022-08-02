function changeColor(IncValue) {
if (IncValue == "1") {
    document.getElementById("act-menu-div-1").style.backgroundColor =
    "#264ECA";
    document.getElementById("act-menu-div-1").style.color = "#ffffff";
    document.getElementById("act-menu-div-2").style.backgroundColor =
    "#ffffff";
    document.getElementById("act-menu-div-2").style.color = "black";
    document.getElementById("act-menu-div-3").style.backgroundColor =
    "#ffffff";
    document.getElementById("act-menu-div-3").style.color = "black";
    document.getElementById("act-menu-div-4").style.backgroundColor =
    "#ffffff";
    document.getElementById("act-menu-div-4").style.color = "black";

    // display and hide divs
    document.getElementById("rent-requests").style.display = "block";
    document.getElementById("ratings").style.display = "none";
    document.getElementById("comments").style.display = "none";
    document.getElementById("rent-lists").style.display = "none";
} 
else if (IncValue == "2") {
    document.getElementById("act-menu-div-1").style.backgroundColor =
    "#ffffff";
    document.getElementById("act-menu-div-1").style.color = "black";
    document.getElementById("act-menu-div-2").style.backgroundColor =
    "#264ECA";
    document.getElementById("act-menu-div-2").style.color = "#ffffff";
    document.getElementById("act-menu-div-3").style.backgroundColor =
    "#ffffff";
    document.getElementById("act-menu-div-3").style.color = "black";
    document.getElementById("act-menu-div-4").style.backgroundColor =
    "#ffffff";
    document.getElementById("act-menu-div-4").style.color = "black";

    // display and hide divs
    document.getElementById("rent-requests").style.display = "none";
    document.getElementById("ratings").style.display = "block";
    document.getElementById("comments").style.display = "none";
    document.getElementById("rent-lists").style.display = "none";
} 
else if (IncValue == "3") {
    document.getElementById("act-menu-div-1").style.backgroundColor =
    "#ffffff";
    document.getElementById("act-menu-div-1").style.color = "black";
    document.getElementById("act-menu-div-2").style.backgroundColor =
    "#ffffff";
    document.getElementById("act-menu-div-2").style.color = "black";
    document.getElementById("act-menu-div-3").style.backgroundColor =
    "#264ECA";
    document.getElementById("act-menu-div-3").style.color = "#ffffff";
    document.getElementById("act-menu-div-4").style.backgroundColor =
    "#ffffff";
    document.getElementById("act-menu-div-4").style.color = "black";

    // display and hide divs
    document.getElementById("rent-requests").style.display = "none";
    document.getElementById("ratings").style.display = "none";
    document.getElementById("comments").style.display = "block";
    document.getElementById("rent-lists").style.display = "none";
} 
else if (IncValue == "4") {
    document.getElementById("act-menu-div-1").style.backgroundColor =
    "#ffffff";
    document.getElementById("act-menu-div-1").style.color = "black";
    document.getElementById("act-menu-div-2").style.backgroundColor =
    "#ffffff";
    document.getElementById("act-menu-div-2").style.color = "black";
    document.getElementById("act-menu-div-3").style.backgroundColor =
    "#ffffff";
    document.getElementById("act-menu-div-3").style.color = "black";
    document.getElementById("act-menu-div-4").style.backgroundColor =
    "#264ECA";
    document.getElementById("act-menu-div-4").style.color = "#ffffff";

    document.getElementById("rent-requests").style.display = "none";
    document.getElementById("ratings").style.display = "none";
    document.getElementById("comments").style.display = "none";
    document.getElementById("rent-lists").style.display = "block";
}
}
