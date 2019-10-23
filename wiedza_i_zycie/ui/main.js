
/**
[+] musisz się zdecydować CamelCase czy under_score_case czy whatever case
[+] rozdziel funkcje według tego co robią
[] funkcje które dodają coś do strony --> coś wizualnego przerzuć do pliku `view.js`
[] w `main.js` już tylko wywołuj funkcje
[] powinniśmy mieć tylko jeden modal i jak ktoś KLIKA w okładkę wówczas ładujemy do tego
   modalu ON THE FLY zdjęcia z tego numeru i wyświetlamy
[] musisz zgrupować główne kroki --> main.js
[+] nie potrzebujesz SVG!
[] staraj się zbierać tzw. event handlery i event binding w jednym miejscu
**/


// var logoWidth = document.getElementById("img1").naturalWidth;


  let logoD3El = d3.select('#logo')
  let editionasD3El = d3.selectAll('.editionImg')
  let logoEl = document.getElementById("logo")
  let editionasEl = document.getElementsByClassName("editionImg")

  logoEl.onclick = changeToEditions;
  appendImages();


  // change display functions

  function changeToEditions(){
    logoD3El.style("display", "none");
    // editionasD3El.style("display", "block"); ?????????????????????
    d3.selectAll('.editionImg').style("display", "block");
  }  

  // append functions

  function appendImg(elementId, imag, btId, pos){
    d3.select("#"+elementId.toString())
    .append("img")
    .attr("class", "editionImg")
    .attr("src", "../data/images/"+imag.toString())
    .style("left", pos.x+"px")
    .style("top", pos.y+"px")
    .attr("id", "btn"+btId.toString())
    .on('click', function(d,i){ activeModal( "btn"+btId.toString() ) })
  }
  
  function appendArticleImg(imag, btId){
    d3.select("#mdc"+btId)
    .append("img")
    .attr("src", "../data/images/"+imag.toString())
    .attr("class", "articleImg")
  }

  function appendImages(){

    var pos = {
      x: 0,
      y: 10,
    }
    rowLength = Math.ceil(Math.sqrt(editions.length));
    
    editions.forEach((edition, i) => {
      if( i % rowLength == 0){
        pos.x = 40
        pos.y += 220;
        j = 0;
      }
      pos.x += 170;
      appendImg("editionsImgs", edition["image"], i, pos);
      // appendModal(i);
  
      edition["articles"].forEach(function(article){
        if(article["image"]){
          appendArticleImg(article["image"], i);
        }
      });
    });
  }

  //activate functions

  (() => {
    let parentEl = d3.select('#editionsImgs');
    let childEl = d3.selectAll('.editionImg');

    parentEl.call(
      d3.zoom().on('zoom', () => {
        let t = d3.event.transform;

        childEl.style(
          'transform',
          `translate(${t.x}px, ${t.y}px) scale(${t.k})`);

      }));

  })();

function activeModal(buttonId){
  var modal = document.getElementById("modal");
  var btn = document.getElementById(buttonId);

  btn.onclick = function() {
    modal.style.display = "block";
  }

  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
}


/**
 * MAIN
 */

//wywołanie funkcji
