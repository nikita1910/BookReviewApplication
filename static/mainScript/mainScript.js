$( document ).ready(function() {
try{
    console.log( "Page loaded" );

    /*-- Data table --*/
     $('#dtBasicExample').DataTable({
        "pagingType": "simple"
     });
  $('.dataTables_length').addClass('bs-select');

  /*-- Tooltip --*/
  $('[data-toggle="tooltip"]').tooltip();

  }
  catch(err){
        console.log("Error occurred in page load.\t" + err );
   }

});

checkRadio = (value) => {
try{
   console.log( "Rating: " + value );
   document.getElementById('ratingVal').innerHTML = value;
   document.getElementById('ratingVal').style.display = "none";
   }
   catch(err){
        console.log("Error occurred in checkRadio().\t" + err );
   }
}

validateLogin = (value) => {
     let flag = false
    try{
     for(let i =0; i< value.length;i++){
        if(value[i].trim().toString() == document.getElementById('txtemailid').value.trim().toString()){
            flag = true
            break;
        }
    }
    if (flag== true){
     document.getElementById('lblpasswordcheck').style.display = "none";
    }
    else{
        document.getElementById('lblpasswordcheck').innerHTML = 'No account found with this Email ID'
        document.getElementById('lblpasswordcheck').style.display = "block";
        document.getElementById('lblpasswordcheck').style.color = "Red";
    }
    }
    catch(err){
         console.log("Error occurred in validateLogin().\t" + err );
    }
}

validatePassword = () => {
try{
    if(document.getElementById('txtNewPwd').value != document.getElementById('txtConfirmNewPwd').value){
        document.getElementById('lblpasswordcheck').innerHTML = 'Please enter same password'
         document.getElementById('lblpasswordcheck').style.display = "block";
        document.getElementById('lblpasswordcheck').style.color = "Red";
    }
    else{
        document.getElementById('lblpasswordcheck').style.display = "none";
    }
    }
     catch(err){
         console.log("Error occurred in validatePassword().\t" + err );
    }
}

validateEmail = (emailVal) => {
try{
    var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;

        if (reg.test(emailVal.value) == false)
        {
            alert('Please enter valid Email ID.');
            return false;
        }

        return true;
}
catch(err){
    console.log("Error occurred in validateEmail().\t" + err)
}
}

validateNewEmailID = (value) => {
console.log("In validateEmailID")
     let flag = false
    try{

    //console.log(value)
    //alert(document.getElementById('txtNewEmailID').value)
     for(let i =0; i< value.length;i++){
        if(value[i].trim().toString() == document.getElementById('txtNewEmailID').value.trim().toString()){
            flag = true
            break;
        }
    }
    if (flag== true){
      document.getElementById('lblEmailIdErrMsg').innerHTML = 'Account with this email id already present. Please, choose another.'
        document.getElementById('lblEmailIdErrMsg').style.display = "block";
        document.getElementById('lblEmailIdErrMsg').style.color = "Red";

    }
    else{
       document.getElementById('lblEmailIdErrMsg').style.display = "none";
    }
    }
    catch(err){
         console.log("Error occurred in validateEmailID().\t" + err );
    }
}

/*---Start Nav bar function ---*/
openNav = () => {
    document.getElementById("mySidenav").style.width = "165px";
}

closeNav = () => {
  document.getElementById("mySidenav").style.width = "0";
}
/*---End Nav bar function ---*/


ClearErrorMsg = () => {
try{
    document.getElementById("lblError").innerHTML = "";
}
catch(err){
    console.log("Error occurred in ClearErrorMsg().\t" + err)
}
}
