
/**

[] musisz się zdecydować CamelCase czy under_score_case czy whatever case
[] rozdziel funkcje według tego co robią
[] funkcje które dodają coś do strony --> coś wizualnego przerzuć do pliku `view.js`
[] w `main.js` już tylko wywołuj funkcje
[] powinniśmy mieć tylko jeden modal i jak ktoś KLIKA w okładkę wówczas ładujemy do tego
   modalu ON THE FLY zdjęcia z tego numeru i wyświetlamy
[] musisz zgrupować główne kroki --> main.js
[] nie potrzebujesz SVG!

**/
function displayWindowSize(){

  var window_width = window.innerWidth;
  var window_height = window.innerHeight;

  // @piotrek: to nie zawsze zadziała.
  // @piotrek: uzyj eventu `load` LUB flexbox: https://css-tricks.com/snippets/css/a-guide-to-flexbox/#flexbox-background
  var logo_width = document.getElementById("img1").naturalWidth;
  var logo_height = document.getElementById("img1").naturalHeight;

  setLogo(window_width, window_height, logo_width, logo_height);
}

window.addEventListener("resize", function(){
  displayWindowSize()
});

// @piotrek: cała ta funkcja może być zastąpione czystym CSS
function setLogo(window_width, window_height, logo_width, logo_height){
  d3.select("#logo")
  .style("position", "absolute")  // @piotrek: coś takiego możesz dodać w css
  .style("top", ((window_height-logo_height)/2).toString()+"px")
  .style("left", ((window_width-logo_width)/2).toString()+"px")

  // @piotrek: staraj się zbierać tzw. event handlery i event binding w jednym miejscu
  /**
    np.

    let logoD3El = d3.select('#logo');
    let editionasD3El = d3.select('#editions');

    logoD3El.on('click', hideLogo);

    function hideLogo() {
      logoEl.style("display", "none")
      editionasEl.style("display", "block")
    }
  */
  .on('click', function(d,i){
    d3.select("#logo").style("display", "none")
    d3.select("#editions").style("display", "block")
  })

}

function appendArticleImg(imag, bt_id){

  d3.select("#mdc"+bt_id)
  .append("img")
  .attr("src", "../data/images/"+imag.toString())

  // @piotrek: przerzuć do css jako `class`
  .attr("height", "auto")
  .attr("width", "200px")
  .style("margin-left", "30px")
  .style("margin-top", "20px")
}

var svg = d3.select("#main-container")
  .append("svg")
    .attr("id", "editions")
    // @piotrek: przerzuć do css jako `class`
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

function printImages(){

  // @piotrek: bo co zamieniać `editions` na `myObj` ?
  // @piotrek: patrząc na zmienną `myObj`, o czymś byś pomyślał? co przechowujemy
  // w tej zmiennej?
  var myObj = editions;

  var pos = {
    x: 40,
    y: -50,
  }
  // @piotrek: `editions` --> `myObj` bo to żeby `myObj.length` nazwać
  // `edition_count` ;-)
  // @piotrek ale po co ci właściwie ta zmienna?
  var edition_count = myObj.length;
  var row = Math.ceil(Math.sqrt(edition_count))

  // @piotrek: tych też nie potrzebujesz może je wyczytać z `forEach`
  /**
    ['a', 'b'].forEach(x => {
      console.log(x);
    });

    oraz

    ['a', 'b'].forEach((x, i) => {
      console.log(x, i);
    });

  */
  // var row_pos = 0;
  // var ed_bt_id=0;

  myObj.forEach(edition => {
    if(row_pos>=row){
      pos.x = 40
      pos.y += 110;
      row_pos = 0;
    }
    pos.x += 90;
    appendImg("editions", edition["image"], ed_bt_id, pos);
    appendModal(ed_bt_id);

    edition["articles"].forEach(function(article){
      if(article["image"]){
        appendArticleImg(article["image"], ed_bt_id);
      }
    });
    // ed_bt_id += 1;
    // row_pos += 1;
  });
}

// @piotrek: to powinno być wywołane w jakimś widocznym miejscu
printImages();

function appendImg(element_id, imag, bt_id, pos){
  svg
  // d3.select("#"+element_id.toString())
  .append("image")
  .attr("xlink:href", "../data/images/"+imag.toString())

  // @piotrek: przerzuć do css jako `class`
  .attr("height", "100px")
  .attr("width", "100px")
  // dotąd

  .attr("x", pos.x+"px")
  .attr("y", pos.y+"px")
  .attr("id", "btn"+bt_id.toString())
  .on('click', function(d,i){ activeModal("md"+bt_id.toString(), "btn"+bt_id.toString())  })
}

function appendModal(ed_bt_id){

  d3.select("#modals")
  .append("div")
  .attr("class", "modal")
  .attr("id", "md"+ed_bt_id.toString())

  d3.select("#md"+ed_bt_id.toString())
  .append("div")
  .attr("class", "modal-content")
  .attr("id", "mdc"+ed_bt_id)

}

function activeModal(modalId, buttonId){
  var modal = document.getElementById(modalId);
  var btn = document.getElementById(buttonId);
  // var span = document.getElementsByClassName("close")[0];

  btn.onclick = function() {
    modal.style.display = "block";
  }
  // span.onclick = function() {
  //   modal.style.display = "none";
  // }
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
}


/**
 * MAIN
 */
$(displayWindowSize);
