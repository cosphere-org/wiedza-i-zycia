
var m_c_pos = 0.1;
var m_c = "main-container";

function displayWindowSize(m_c){

  var window_width = window.innerWidth;
  var window_height = window.innerHeight;
    
  document.getElementById(m_c).style.top = (window_height*m_c_pos).toString() + "px"; 
  document.getElementById(m_c).style.left = (window_width*m_c_pos).toString() + "px";
}
 
window.addEventListener("resize", function(){
  displayWindowSize(m_c)
});
displayWindowSize(m_c);

var xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    var myObj = JSON.parse(this.responseText);

      var pos = {
        x: 40,
        y: -50,
      }
      var edition_count = myObj.length;
      var row = Math.ceil(Math.sqrt(edition_count))
      console.log(row)
      var row_pos = 0;
      myObj.forEach(function(edition) {
        if(row_pos>=row){
          pos.x = 40
          pos.y += 110;
          row_pos = 0;
        }
        pos.x += 90;
        appendImg(edition["image"], pos);
        row_pos += 1;
        // console.log(edition["image"])
        edition["articles"].forEach(function(article){
          // console.log(article)
        });
      });
    // console.log(myObj[0]["articles"][0]);
  }
};
xmlhttp.open("GET", "editions.json", true);
xmlhttp.send();

var svg = d3.select("#main-container")
  .append("svg")
    .attr("width",  "100%")
    .attr("height",  "100%")
  .append("g")

  d3.select("#main-container")
    .call(
    d3.zoom()
    .on("zoom", function () {
      if(d3.event.transform.k>0.5){
        svg.attr("transform", d3.event.transform)
      }
}))

d3.select("#main-container")
    .call(
    d3.zoom()
    .on("zoom", zoomed),
    )
    g = svg.select("g"),
    x0 = +svg.attr("x"),
    y0 = +svg.attr("y"),
    x1 = +svg.attr("width") + x0,
    y1 = +svg.attr("height") + y0;
    width = +svg.attr("width"),
    height = +svg.attr("height"),

function zoomed() {
  var t = d3.event.transform;
  if (t.invertX(0) > x0) t.x = -x0 * t.k;
  else if (t.invertX(width) < x1) t.x = width - x1 * t.k;
  if (t.invertY(0) > y0) t.y = -y0 * t.k;
  else if (t.invertY(height) < y1) t.y = height - y1 * t.k;
  g.attr("transform", t);
}

function appendImg(imag, pos){
  svg
  .append("image")
  .attr("xlink:href", "images/"+imag.toString())
  .attr("height", "100px")
  .attr("width", "100px")
  .attr("x", pos.x+"px")
  .attr("y", pos.y+"px")
}