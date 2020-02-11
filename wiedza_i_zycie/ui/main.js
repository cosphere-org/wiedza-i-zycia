
(() => {

  let editions = new EditionsGridComponent(data);
  editions.render();

  let logo = new LogoComponent();
  logo.el.onclick = () => {
    logo.hide();
    editions.show();
  }

  let modal = new ModalComponent();
  // modal.render();

  modal.el.onclick = (event) => {
    modal.show()
    modal.hide(event)
  }

  editions.d3El.nodes().forEach((edition, i) => {
    edition.onclick = (event) => {
      modal.show();
      // console.log('SHOW ARTICLES', data[parseInt(event.target.dataset.editionidx)].articles);
      let articles = data[parseInt(event.target.dataset.editionidx)].articles;
      articles.forEach( (article) => {

        modal.addArticleImg(article);
      });
    }
  });

})();
