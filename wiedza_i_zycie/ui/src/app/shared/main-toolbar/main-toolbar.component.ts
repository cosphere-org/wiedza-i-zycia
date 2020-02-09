import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-main-toolbar',
  templateUrl: './main-toolbar.component.html',
  styleUrls: ['./main-toolbar.component.scss']
})
export class MainToolbarComponent implements OnInit {

  sideBarIsOpened = false;

  constructor() { }

  ngOnInit() {
  }

  toggleSideBar(shouldOpen: boolean) {
    console.log('000');
    this.sideBarIsOpened = !this.sideBarIsOpened;
  }

}
