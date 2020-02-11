
class LogoComponent {

  get d3El() {
    return d3.select('#logo');
  }

  get el() {
    return document.getElementById("logo");
  }

  hide () {
    this.d3El.style('display', 'none');
  }

  render () {
    this.el.onclick = this.onClick(); // ask for that
  }
}

class ModalComponent {

  get d3El() {
    return d3.select('#modal');
  }

  get el() {
    return document.getElementById('modal');
  }

  get d3ELcontent() {
    return d3.select('#modalContent');
  }

  hide (event) {
    if (event.target != this.d3El){
      this.d3El.style('display', 'none');
    }
    // ???????????????????????????????????????
    removeArticleImgs ();
  }

  show () {
    this.d3El.style('display', 'block');
  }

  addArticleImg (artImag) {
    // console.log(artImag);
    this.d3ELcontent.append('img')
      .attr('src', `../data/images/${artImag['image']}`)
      .attr('height', '200px')
      .attr('width', '200px')
  }

  removeArticleImgs () {
    console.log('remove');
    this.d3ELcontent.removeAll('img');
  }

  render () {
    this.el.onclick = this.onClick(); // ask for that
  }

  // activeModal(buttonId){
  //   var modal = document.getElementById("modal");
  //   var btn = document.getElementById(buttonId);
  
  //   btn.onclick = function() {
  //     modal.style.display = "block";
  //   }
  
  //   window.onclick = function(event) {
  //     if (event.target == modal) {
  //       modal.style.display = "none";
  //     }
  //   }
  // }

}
