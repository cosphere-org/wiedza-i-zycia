
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

(() => {

  let editions = new EditionsGridComponent(data);
  editions.render();

  let logo = new LogoComponent();
  logo.el.onclick = () => {
    logo.hide();
    editions.show();
  }

  editions.d3El.nodes().forEach((edition, i) => {
    edition.onclick = (event) => {
      console.log('SHOW ARTICLES', data[parseInt(event.target.dataset.editionidx)].articles);
    }
  });

})();
