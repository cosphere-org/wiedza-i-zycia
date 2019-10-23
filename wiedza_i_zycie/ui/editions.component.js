
class EditionsGridComponent {

  constructor(data) {
    this.data = data;
  }

  get d3El() {
    return d3.selectAll('.editionImg');
  }

  get parentd3El() {
    return d3.select('#editionsImgs');
  }

  show() {
    this.d3El.style('display', 'block');
  }

  /**
   * RENDERING
   */
  render () {

    let pos = {
      x: 0,
      y: 10,
    };
    let rowLength = Math.ceil(Math.sqrt(this.data.length));

    this.data.forEach((editionData, i) => {
      if( i % rowLength == 0){
        pos.x = 40
        pos.y += 220;
      }
      pos.x += 170;

      this.renderEdition(editionData, i, pos);

      editionData.articles.forEach(article => {
        if(article.image){
          // this.renderArticleImage(article.image, i);
        }
      });
    });

    this.activaZoom();
  }

  renderEdition(editionData, editionIdx, pos) {
    this
      .parentd3El
      .append('img')
      .attr('class', 'editionImg')
      .attr('src', `../data/images/${editionData.image}`)
      .style('left', `${pos.x}px`)
      .style('top', `${pos.y}px`)
      .attr('data-editionIdx', editionIdx)
      .attr('id', this.getEditionId(editionIdx));
      // .on('click', () => {
      //   activeModal(imageIdx)
      // });
  }

  getEditionId(idx) {
    return `btn-${idx}`;
  }

  // renderArticleImage(imagePath, imageIdx){
  //   d3.select(`#mdc${(imageIdx)}`)
  //   .append('img')
  //   .attr('src', `../data/images/{imagePath}`)
  //   .attr('class', 'articleImg')
  // }

  /**
   * BEHAVIOUR
   */
  activaZoom() {
    this.parentd3El.call(
      d3.zoom().on('zoom', () => {
        let t = d3.event.transform;

        this.d3El.style(
          'transform',
          `translate(${t.x}px, ${t.y}px) scale(${t.k})`);
      }));
  }

  activeModal(buttonId){
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
}
