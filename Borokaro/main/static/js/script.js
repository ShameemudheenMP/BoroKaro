function validateForm() {
    let x = document.forms["SignUp"]["name"].value;
    
    if (x == "") {
      alert("Name must be filled out.");
      return false;
    }

    x = document.forms["SignUp"]["email"].value;
    console.log(x)
    if (x.length == 0) {
      alert("Email must be filled out.");
      return false;
    }

    x = document.forms["SignUp"]["password"].value;
    if (x == "") {
      alert("Password must be filled out.");
      return false;
    }
    else if(x.length < 8){
        alert("Password must contain at least 8 chararacters!")
        return false;
    }

    x = document.forms["SignUp"]["phoneno"].value;
    if (x == "") {
      alert("Phone number must be filled out.");
      return false;
    }
    else if(x.length < 10){
        alert("Please enter a valid phone number.")
        return false;
    }

    x = document.forms["SignUp"]["states"].value;
    console.log("state : ", x)
    if (x == "") {
      alert("State must be selected.");
      return false;
    }

    x = document.forms["SignUp"]["districts"].value;
    console.log("district : ", x)
    if (x == "") {
      alert("District must be selected.");
      return false;
    }

}