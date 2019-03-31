
function addToList() {
    var current = document.getElementById("entrylist").innerHTML; 
    document.getElementById("entrylist").innerHTML = current + '<li> <div class="card"> <div class="card-content"> <div class="content"> <h1 class="title">Title</h1><time datetime="2016-1-1">11:09 PM - 1 Jan 2016</time></div> <div> <footer class="card-footer"> <a href="#" class="card-footer-item"> <i class="fa fa-book"></i> ‏‏‎ View Entry</a> </footer></div></div></li>';
}