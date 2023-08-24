// let user = '<%- JSON.stringify(user) %>';
// user = JSON.parse(user);

function color(status, id1) {
  let upbutton = document.getElementById("up/" + id1);
  let downbutton = document.getElementById("down/" + id1);
  if (status === "upvoted") {
    upbutton.style.color = "lime";
    downbutton.style.color = "black";
  }
  else if (status === "downvoted") {
    downbutton.style.color = "red";
    upbutton.style.color = "black";
  }
  else {
    downbutton.style.color = "black";
    upbutton.style.color = "black";
  }
}

function add_verified(votes,id1) {
  let verified0 = document.getElementById("verified0/"+id1);
  let verified1 = document.getElementById("verified1/"+id1);
  if (votes >= 1) {
    if (verified0) {
      verified0.innerHTML = "";
      verified0.style.marginLeft = "0px";
    }
    verified1.style.marginLeft = "1%";
    verified1.innerHTML = "&check;";
  }
  else {
    if (verified0) {
      verified0.innerHTML = "";
      verified0.style.marginLeft = "0px";
    }
    if (verified1) {
      verified1.innerHTML = "";
      verified1.style.marginLeft = "0px";
    }
  }

}

let verified = document.getElementById("verified");
function upclick(id) {
  const id1 = id.split("/")[1];
  console.log("clicked");
  fetch('/myApp/upvote/' + id1, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    }
    // body: JSON.stringify({ id1, userid: user._id }),
  })
    .then((res) => res.json())
    .then((data) => {
      const voteCount = document.getElementById("vc/" + id1);
      voteCount.innerHTML = (data.votes);
      color(data.status, id1)
      add_verified(data.votes,id1);
    })
    .catch((err) => {
      console.error(err);
    });
}

function downclick(id) {
  const id1 = id.split("/")[1];
  console.log(id1);
  fetch('/myApp/downvote/' + id1, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    }
    // body: JSON.stringify({ id1, userid: user._id }),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      const voteCount = document.getElementById("vc/" + id1);
      voteCount.innerHTML =(data.votes);
      color(data.status, id1)
      add_verified(data.votes,id1);
    })
    .catch((err) => {
      console.error(err);
    });
}
