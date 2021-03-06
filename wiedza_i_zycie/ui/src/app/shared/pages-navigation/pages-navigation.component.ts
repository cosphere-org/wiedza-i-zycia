import { Component, OnInit, HostBinding, Input } from '@angular/core';

@Component({
  selector: 'app-pages-navigation',
  templateUrl: './pages-navigation.component.html',
  styleUrls: ['./pages-navigation.component.scss']
})
export class PagesNavigationComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

  @HostBinding('class.is-open') @Input()
  isOpen = false;

  closeNav() {
    this.isOpen = !this.isOpen;
  }

}
