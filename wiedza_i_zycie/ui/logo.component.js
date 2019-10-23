
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
    this.el.onclick = this.onClick();
  }
}
