# example/urls.py
from django.urls import path

from example.views import index,python_file


urlpatterns = [
    path('', index),
    path('python_file', python_file,name='python_file'),
]


# <div>
#         <a href="/runscript"
#       ><button onclick="button()" styles="background-color: #57927a; width: 300px; box " type="button">Run python script</button></a
#     </div>
#   <script src="http://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>

# // function gotoPython(){
#           //     $.ajax({
#           //       url: "/python_file",  
#           //      context: document.body
#           //     }).done(function() {
#           //      alert('finished python script');;
#           //      window.location.href = "/scrapedarticles.html";
#           //     }); 
#           // }