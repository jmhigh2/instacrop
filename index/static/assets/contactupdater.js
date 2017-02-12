function createContact(idNum, user) {
  // magic creation of contact
  var formData = new FormData();

  var createId = "#create" + idNum;
  var updateId = "#update" + idNum;
  var nameId = "#name" + idNum;
  var numberId = "#number" + idNum;
  var name = $(nameId).val();
  var number = $(numberId).val();
  formData.append("name", name);
  formData.append("user", user);
  formData.append("phone", number); // number 123456 is immediately converted to a string "123456"

  var content = '<a id="a"><b id="b">hey!</b></a>'; // the body of the new file...
  var blob = new Blob([content], { type: "text/xml"});

  formData.append("webmasterfile", blob);

  var request = new XMLHttpRequest();
  request.open("POST", "http://gcphoto.herokuapp.com/create");
  request.send(formData);

  $(createId).remove();
  $(updateId).remove();

}

function updateContact(idNum, user) {
  // magic creation of contact
  var formData = new FormData();

  var createId = "#create" + idNum;
  var updateId = "#update" + idNum;
  var nameId = "#name" + idNum;
  var numberId = "#number" + idNum;
  var name = $(nameId).val();
  var number = $(numberId).val();
  formData.append("name", name);
  formData.append("user", user);
  formData.append("phone", number); // number 123456 is immediately converted to a string "123456"

  var content = '<a id="a"><b id="b">hey!</b></a>'; // the body of the new file...
  var blob = new Blob([content], { type: "text/xml"});


  var request = new XMLHttpRequest();
  request.open("POST", "http://127.0.0.1:8000/update");
  request.send(formData);

  $(createId).remove();
  $(updateId).remove();


}
