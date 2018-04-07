 /*function chooseBoard(idNumber){
    document.getElementById("toAnotherSelect").innerHTML = idNumber;
    document.getElementById("mySelect").options.length = 0
    var x = document.getElementById("mySelect");
    var length = x.options.length;
    if(idNumber ==0){
        var c = document.createElement("option");
         c.text = "--NONE--";
         x.options.add(c, 0);
    }else if(idNumber==1){
         for(i=0;i<20;i++){
            var c = document.createElement("option");
            c.text = i;
            x.options.add(c, i);
         }
    }else{
        for(i=0;i<8;i++){
            var c = document.createElement("option");
            c.text = i;
            x.options.add(c, i);
        }
    }
   document.getElementById("toAnotherSelect").innerHTML = length;
}*/
 
function chooseBoard(idNumber){
    //document.getElementById("toAnotherSelect").innerHTML = idNumber;
    var x = document.getElementById("pin");
    var len = x.options.length;
    for(var i=len-1;i>=0;i--){
        x.options[i]=null;
    }
    if(idNumber == 0){
        var c = document.createElement("option");
         c.text = "--NONE--";
         x.options.add(c, 0);
    }else if(idNumber==1){
         for(i=0;i<20;i++){
            var c = document.createElement("option");
            c.text = i;
            x.options.add(c, i);
         }
    }else{
        for(i=0;i<8;i++){
            var c = document.createElement("option");
            c.text = i;
            x.options.add(c, i);
        }
    }
    len = x.options.length; //aktualna dlugosc
   //document.getElementById("toAnotherSelect").innerHTML = len;
}

function checkAll(){
    var checkBoxAll = document.getElementsByName("selectAll")[0];
    var checkBoxSelect = document.getElementsByName("selectThis[]");
   
    if(checkBoxAll.checked == false){
        for(var i=0;i<checkBoxSelect.length;i++){
            checkBoxSelect[i].checked = false;
        }
    }
    else{
        for(var i=0;i<checkBoxSelect.length;i++){
            checkBoxSelect[i].checked = true;
        }
    }
}
